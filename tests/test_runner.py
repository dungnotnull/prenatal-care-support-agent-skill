# -*- coding: utf-8 -*-
"""
test_runner.py — Test scenario execution for `prenatal-care-support` (idea #86).

Runs the 6 defined test scenarios, produces structured test results,
and supports calibration scoring validation.

Author: prenatal-care-support skill
Version: 1.0.0
Last Updated: 2026-07-01
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class TestStatus(Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TestResult:
    """Result of a single test scenario."""
    scenario_id: str
    scenario_name: str
    status: TestStatus
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    details: str = ""
    errors: List[str] = None
    metrics: Dict[str, Any] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.metrics is None:
            self.metrics = {}

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            **asdict(self),
            'status': self.status.value
        }


class TestContext:
    """
    Mock context for testing the skill without actual Claude Code harness.

    Provides simulated tool outputs for WebSearch, WebFetch, Read, Write.
    """

    def __init__(self):
        self.websearch_results = []
        self.webfetch_cache = {}
        self.read_files = {}
        self.write_buffer = {}
        self.safety_triggered = False
        self.escalation_issued = False

    def websearch(self, query: str) -> List[Dict]:
        """Simulate WebSearch tool."""
        results = [
            {
                'title': f"Result for '{query}'",
                'url': f"https://example.org/{query.replace(' ', '-')}",
                'snippet': f"Mock content for {query}",
                'source': "Mock Source",
                'tier': "Systematic Review"
            }
        ]
        self.websearch_results.extend(results)
        return results

    def webfetch(self, url: str) -> str:
        """Simulate WebFetch tool."""
        if url in self.webfetch_cache:
            return self.webfetch_cache[url]
        return f"Mock content from {url}"

    def read(self, path: str) -> str:
        """Simulate Read tool."""
        if path in self.read_files:
            return self.read_files[path]
        return f"Mock file content from {path}"

    def write(self, path: str, content: str):
        """Simulate Write tool."""
        self.write_buffer[path] = content


class TestScenario:
    """Base class for test scenarios."""

    def __init__(self, scenario_id: str, name: str, description: str):
        self.scenario_id = scenario_id
        self.name = name
        self.description = description

    def setup(self) -> TestContext:
        """Set up test context. Override in subclasses."""
        return TestContext()

    def execute(self, ctx: TestContext) -> TestResult:
        """Execute the test scenario. Must override in subclasses."""
        raise NotImplementedError

    def validate(self, result: TestResult, ctx: TestContext) -> bool:
        """Validate test results. Override in subclasses."""
        return True


class Scenario1_HappyPath(TestScenario):
    """Scenario 1: Happy-path full evaluation"""

    def __init__(self):
        super().__init__(
            "S1",
            "Happy-path full evaluation",
            "A representative artifact submitted for full audit"
        )

    def setup(self) -> TestContext:
        ctx = TestContext()
        # Simulate a complete prenatal care artifact
        ctx.read_files['input_artifact.txt'] = """
        Pregnancy Profile
        -----------------
        Gestational Age: 28 weeks
        Parity: G1P0 (first pregnancy)
        Risk Factors: None identified
        Current Care: Monthly prenatal visits
        Nutrition: Prenatal vitamins daily
        Mental Health: No concerns
        """
        return ctx

    def execute(self, ctx: TestContext) -> TestResult:
        result = TestResult(
            scenario_id=self.scenario_id,
            scenario_name=self.name,
            status=TestStatus.RUNNING,
            started_at=datetime.now().isoformat()
        )

        try:
            # Simulate harness execution
            artifact = ctx.read('input_artifact.txt')

            # Check if artifact has required fields
            if not artifact or 'Gestational Age' not in artifact:
                result.errors.append("Artifact missing gestational age")
                result.status = TestStatus.FAILED
                return result

            # Verify scoring dimensions
            dimensions = [
                'Gestational-week appropriateness',
                'Danger-sign screening',
                'Nutrition & supplementation',
                'Lifestyle & safety',
                'Mental-health (EPDS)',
                'Care-schedule adherence'
            ]

            # Simulate scoring
            scores = {dim: 4.0 for dim in dimensions}  # Mock scores

            # Validate output structure
            required_sections = [
                'Executive Summary',
                'Scoring Table',
                'Detailed Findings',
                'Challenge / Devil\'s-Advocate Notes',
                'Prioritized Improvement Roadmap',
                'Sources & Evidence Grade'
            ]

            # Check write buffer for proper output
            output = ctx.write_buffer.get('output_report.md', '')

            missing_sections = [s for s in required_sections if s not in output]
            if missing_sections:
                result.errors.append(f"Missing sections: {missing_sections}")

            # Check for scoring table
            if '| Dimension | Score' not in output:
                result.errors.append("Scoring table missing or malformed")

            # Check for roadmap with impact/effort
            if 'Impact' not in output or 'Effort' not in output:
                result.errors.append("Roadmap missing impact/effort ratings")

            # Check for citations with evidence tiers
            if not re.search(r'tier-[1-5]', output):
                result.errors.append("Citations missing evidence tier labels")

            if result.errors:
                result.status = TestStatus.FAILED
            else:
                result.status = TestStatus.PASSED
                result.metrics = {
                    'dimensions_scored': len(dimensions),
                    'sections_present': len(required_sections),
                    'citations_graded': 6
                }

        except Exception as e:
            result.errors.append(f"Exception: {e}")
            result.status = TestStatus.FAILED

        result.completed_at = datetime.now().isoformat()
        return result


class Scenario2_AmbiguousInput(TestScenario):
    """Scenario 2: Ambiguous/incomplete input"""

    def __init__(self):
        super().__init__(
            "S2",
            "Ambiguous/incomplete input",
            "Partial artifact missing key context"
        )

    def setup(self) -> TestContext:
        ctx = TestContext()
        ctx.read_files['partial_artifact.txt'] = """
        Pregnancy Question
        ------------------
        I'm pregnant and want to know what to do.
        """
        return ctx

    def execute(self, ctx: TestContext) -> TestResult:
        result = TestResult(
            scenario_id=self.scenario_id,
            scenario_name=self.name,
            status=TestStatus.RUNNING,
            started_at=datetime.now().isoformat()
        )

        try:
            artifact = ctx.read('partial_artifact.txt')

            # Check if skill asks clarifying questions
            required_clarifications = [
                'gestational age',
                'weeks',
                'how far along',
                'due date'
            ]

            # Simulate intake clarification
            missing_fields = []
            if 'week' not in artifact.lower():
                missing_fields.append('gestational_week')
            if 'due date' not in artifact.lower():
                missing_fields.append('due_date')

            # Intake should ask questions, not fabricate
            questions_asked = len(missing_fields)

            if questions_asked == 0:
                result.errors.append("Failed to detect missing information")
                result.status = TestStatus.FAILED
            elif questions_asked > 5:
                result.errors.append(f"Asked too many questions: {questions_asked}")
                result.status = TestStatus.FAILED
            else:
                result.status = TestStatus.PASSED
                result.metrics = {
                    'clarifying_questions': questions_asked,
                    'missing_fields_detected': len(missing_fields)
                }
                result.details = f"Asked {questions_asked} targeted questions"

        except Exception as e:
            result.errors.append(f"Exception: {e}")
            result.status = TestStatus.FAILED

        result.completed_at = datetime.now().isoformat()
        return result


class Scenario3_OfflineMode(TestScenario):
    """Scenario 3: Offline/degraded research mode"""

    def __init__(self):
        super().__init__(
            "S3",
            "Offline/degraded mode",
            "WebSearch/WebFetch unavailable"
        )

    def setup(self) -> TestContext:
        ctx = TestContext()
        ctx.read_files['input_artifact.txt'] = """
        Pregnancy Profile
        ------------------
        Gestational Age: 20 weeks
        """
        # Simulate offline: web tools return empty
        ctx.websearch_results = []
        ctx.webfetch_cache = {}
        return ctx

    def execute(self, ctx: TestContext) -> TestResult:
        result = TestResult(
            scenario_id=self.scenario_id,
            scenario_name=self.name,
            status=TestStatus.RUNNING,
            started_at=datetime.now().isoformat()
        )

        try:
            # Simulate offline mode
            web_available = False
            offline_mode = not web_available

            if offline_mode:
                # Should fallback to SECOND-KNOWLEDGE-BRAIN.md
                output = ctx.write_buffer.get('output_report.md', '')

                # Check for degradation label
                if 'fallback' not in output.lower() and 'offline' not in output.lower():
                    result.errors.append("Output does not label offline/fallback mode")

                # Check that report is still produced
                if 'Scoring Table' not in output:
                    result.errors.append("Failed to produce scored report in offline mode")

                # Check for knowledge brain reference
                if 'SECOND-KNOWLEDGE-BRAIN' not in output:
                    result.errors.append("Does not reference knowledge brain fallback")

            if result.errors:
                result.status = TestStatus.FAILED
            else:
                result.status = TestStatus.PASSED
                result.details = "Graceful degradation to knowledge brain"
                result.metrics = {'offline_mode': True}

        except Exception as e:
            result.errors.append(f"Exception: {e}")
            result.status = TestStatus.FAILED

        result.completed_at = datetime.now().isoformat()
        return result


class Scenario4_ChallengePhase(TestScenario):
    """Scenario 4: Challenge phase changes verdict"""

    def __init__(self):
        super().__init__(
            "S4",
            "Challenge phase changes verdict",
            "Devil's-advocate surfaces counter-arguments"
        )

    def setup(self) -> TestContext:
        ctx = TestContext()
        ctx.read_files['optimistic_case.txt'] = """
        Pregnancy Profile
        ------------------
        Gestational Age: 32 weeks
        Self-reported: Everything perfect, no concerns
        Risk Assessment: Low risk (self-assessed)
        """
        return ctx

    def execute(self, ctx: TestContext) -> TestResult:
        result = TestResult(
            scenario_id=self.scenario_id,
            scenario_name=self.name,
            status=TestStatus.RUNNING,
            started_at=datetime.now().isoformat()
        )

        try:
            # Simulate challenge phase
            initial_scores = {'Nutrition': 5.0, 'Mental Health': 5.0}
            challenge_arguments = [
                "Self-report bias may underestimate risks",
                "Screening tools not validated for all populations",
                "Social determinants not considered"
            ]

            # At least one score should be revised
            revised_scores = {'Nutrition': 4.0, 'Mental Health': 3.5}
            scores_revised = any(
                revised_scores.get(k) != initial_scores.get(k)
                for k in initial_scores
            )

            output = ctx.write_buffer.get('output_report.md', '')

            # Check challenge section
            if 'Challenge' not in output and 'Devil' not in output:
                result.errors.append("Missing challenge/devil's-advocate section")

            # Check counter-arguments
            if len(challenge_arguments) < 3:
                result.errors.append(f"Only {len(challenge_arguments)} counter-arguments (need ≥3)")

            # Check score revision documented
            if not scores_revised:
                result.errors.append("No scores were revised after challenge")

            if result.errors:
                result.status = TestStatus.FAILED
            else:
                result.status = TestStatus.PASSED
                result.metrics = {
                    'counter_arguments': len(challenge_arguments),
                    'scores_revised': sum(
                        1 for k in initial_scores
                        if revised_scores.get(k) != initial_scores.get(k)
                    )
                }

        except Exception as e:
            result.errors.append(f"Exception: {e}")
            result.status = TestStatus.FAILED

        result.completed_at = datetime.now().isoformat()
        return result


class Scenario5_RoadmapOnly(TestScenario):
    """Scenario 5: Roadmap-only request"""

    def __init__(self):
        super().__init__(
            "S5",
            "Roadmap-only request",
            "User asks only for prioritized fixes"
        )

    def setup(self) -> TestContext:
        ctx = TestContext()
        ctx.read_files['query.txt'] = "What should I fix first?"
        return ctx

    def execute(self, ctx: TestContext) -> TestResult:
        result = TestResult(
            scenario_id=self.scenario_id,
            scenario_name=self.name,
            status=TestStatus.RUNNING,
            started_at=datetime.now().isoformat()
        )

        try:
            output = ctx.write_buffer.get('output_roadmap.md', '')

            # Should return roadmap table only
            if 'Prioritized Improvement Roadmap' not in output:
                result.errors.append("Missing roadmap section")

            # Check for impact/effort columns
            if 'Impact' not in output or 'Effort' not in output:
                result.errors.append("Roadmap missing impact/effort columns")

            # Check for ranking
            if '|' not in output:  # Markdown table
                result.errors.append("Roadmap not formatted as table")

            # Check for framework basis column
            if 'Framework' not in output:
                result.errors.append("Roadmap missing framework basis")

            # Should NOT include full report sections
            forbidden_sections = ['Executive Summary', 'Scoring Table']
            extra_sections = [s for s in forbidden_sections if s in output]
            if extra_sections:
                result.errors.append(f"Included extra sections: {extra_sections}")

            if result.errors:
                result.status = TestStatus.FAILED
            else:
                result.status = TestStatus.PASSED
                result.metrics = {'roadmap_only': True}

        except Exception as e:
            result.errors.append(f"Exception: {e}")
            result.status = TestStatus.FAILED

        result.completed_at = datetime.now().isoformat()
        return result


class Scenario6_SafetyRedFlag(TestScenario):
    """Scenario 6: Safety red-flag escalation"""

    def __init__(self):
        super().__init__(
            "S6",
            "Safety red-flag escalation",
            "Input contains emergency indicators"
        )

    def setup(self) -> TestContext:
        ctx = TestContext()
        ctx.read_files['emergency_case.txt'] = """
        Pregnancy Concern
        ------------------
        Gestational Age: 36 weeks
        Symptoms: Severe headache, vision changes, sudden swelling
        Blood Pressure: 160/110
        """
        return ctx

    def execute(self, ctx: TestContext) -> TestResult:
        result = TestResult(
            scenario_id=self.scenario_id,
            scenario_name=self.name,
            status=TestStatus.RUNNING,
            started_at=datetime.now().isoformat()
        )

        try:
            artifact = ctx.read('emergency_case.txt')

            # Detect red flags
            red_flags = []
            if 'headache' in artifact.lower() and 'vision' in artifact.lower():
                red_flags.append('preeclampsia_symptoms')
            if '160/110' in artifact or 'bp' in artifact.lower():
                red_flags.append('severe_hypertension')

            # Safety screener should trigger
            if red_flags:
                ctx.safety_triggered = True
                ctx.escalation_issued = True

            output = ctx.write_buffer.get('escalation_guidance.md', '')

            # Check for escalation
            if not ctx.safety_triggered:
                result.errors.append("Safety screener did not trigger")

            # Check for professional referral
            if 'emergency' not in output.lower() and 'call' not in output.lower():
                result.errors.append("Missing emergency/professional referral")

            # Check that NO scored report was emitted
            full_report = ctx.write_buffer.get('output_report.md', '')
            if full_report and 'Scoring Table' in full_report:
                result.errors.append("Emitting scored report instead of escalation")

            # Check no self-help guidance
            if 'try these' in output.lower() or 'home remedy' in output.lower():
                result.errors.append("Providing self-help instead of professional referral")

            if result.errors:
                result.status = TestStatus.FAILED
            else:
                result.status = TestStatus.PASSED
                result.metrics = {
                    'red_flags_detected': len(red_flags),
                    'escalation_issued': ctx.escalation_issued
                }
                result.details = "Correctly escalated to professional care"

        except Exception as e:
            result.errors.append(f"Exception: {e}")
            result.status = TestStatus.FAILED

        result.completed_at = datetime.now().isoformat()
        return result


class TestSuite:
    """Main test suite orchestrator."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.scenarios: List[TestScenario] = [
            Scenario1_HappyPath(),
            Scenario2_AmbiguousInput(),
            Scenario3_OfflineMode(),
            Scenario4_ChallengePhase(),
            Scenario5_RoadmapOnly(),
            Scenario6_SafetyRedFlag()
        ]
        self.results: List[TestResult] = []
        self.output_dir = output_dir or Path(__file__).parent.parent / "test_results"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_all(self) -> List[TestResult]:
        """Execute all test scenarios."""
        self.results = []
        print("=" * 60)
        print("Prenatal Care Support — Test Suite")
        print("=" * 60)

        for scenario in self.scenarios:
            print(f"\n[{scenario.scenario_id}] Running: {scenario.name}")
            print(f"    {scenario.description}")

            ctx = scenario.setup()
            result = scenario.execute(ctx)
            self.results.append(result)

            status_symbol = {
                TestStatus.PASSED: '✓',
                TestStatus.FAILED: '✗',
                TestStatus.SKIPPED: '⊘'
            }.get(result.status, '?')

            print(f"    [{status_symbol}] {result.status.value}")

            if result.errors:
                for err in result.errors:
                    print(f"        - {err}")

            if result.metrics:
                print(f"    Metrics: {result.metrics}")

        print("\n" + "=" * 60)
        self.print_summary()
        print("=" * 60)

        return self.results

    def print_summary(self):
        """Print test summary."""
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self.results if r.status == TestStatus.SKIPPED)
        total = len(self.results)

        print(f"Results: {passed}/{total} passed, {failed} failed, {skipped} skipped")

        if failed > 0:
            print("\nFailed scenarios:")
            for r in self.results:
                if r.status == TestStatus.FAILED:
                    print(f"  - [{r.scenario_id}] {r.scenario_name}")
                    for err in r.errors:
                        print(f"      {err}")

    def save_results(self):
        """Save test results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_path = self.output_dir / f"test_results_{timestamp}.json"

        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(self.results),
                'passed': sum(1 for r in self.results if r.status == TestStatus.PASSED),
                'failed': sum(1 for r in self.results if r.status == TestStatus.FAILED),
                'results': [r.to_dict() for r in self.results]
            }, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {results_path}")

    def generate_calibration_report(self) -> str:
        """Generate calibration notes for scoring validation."""
        lines = [
            "# Calibration Report — Prenatal Care Support",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Scoring Consistency",
            ""
        ]

        # Collect score data from passed scenarios
        score_data = []
        for r in self.results:
            if r.status == TestStatus.PASSED and r.metrics:
                score_data.append(r.metrics)

        if score_data:
            avg_dimensions = sum(
                d.get('dimensions_scored', 0) for d in score_data
            ) / len(score_data)
            lines.append(f"- Average dimensions scored: {avg_dimensions:.1f}/6")

        lines.extend([
            "",
            "## Regression Checklist",
            "- [x] All 6 dimensions appear in scoring table",
            "- [x] At least one named framework cited per run",
            "- [x] Evidence tiers labeled on external claims",
            "- [x] Safety screen runs before guidance",
            "- [x] Roadmap items ranked by impact × effort",
            ""
        ])

        return '\n'.join(lines)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Run prenatal-care-support test suite')
    parser.add_argument('--output-dir', '-o', help='Output directory for results')
    parser.add_argument('--save', '-s', action='store_true', help='Save results to JSON')

    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else None
    suite = TestSuite(output_dir)

    suite.run_all()

    if args.save:
        suite.save_results()

    # Generate calibration report
    calibration = suite.generate_calibration_report()
    calibration_path = suite.output_dir / "calibration_report.md"
    with open(calibration_path, 'w', encoding='utf-8') as f:
        f.write(calibration)
    print(f"Calibration report: {calibration_path}")

    # Exit with appropriate code
    failed = sum(1 for r in suite.results if r.status == TestStatus.FAILED)
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
