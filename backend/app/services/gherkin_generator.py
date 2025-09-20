from typing import Dict, Any, List
import re
from jinja2 import Template

class GherkinGenerator:
    def __init__(self):
        self.feature_template = Template("""Feature: {{ feature_name }}
  {{ description }}

  {% for scenario in scenarios %}
  Scenario: {{ scenario.name }}
    {% for step in scenario.steps %}
    {{ step }}
    {% endfor %}
  {% endfor %}
""")

    def generate_feature(self, parsed_data: Dict[str, Any], feature_name: str, doc_type: str) -> str:
        """Generate Gherkin feature file content from parsed document data."""
        try:
            if doc_type == "User Story":
                return self._generate_from_user_story(parsed_data, feature_name)
            elif doc_type in ["BRD", "FRD"]:
                return self._generate_from_requirements(parsed_data, feature_name)
            elif doc_type == "Test Case":
                return self._generate_from_test_case(parsed_data, feature_name)
            else:
                raise ValueError(f"Unsupported document type: {doc_type}")
        except Exception as e:
            raise ValueError(f"Error generating feature file: {str(e)}")

    def _generate_from_user_story(self, parsed_data: Dict[str, Any]) -> str:
        scenarios = []
        for story in parsed_data["stories"]:
            scenario = {
                "name": f"Implement {story['want']}",
                "steps": [
                    f"Given I am a {story['role']}",
                    f"When I {story['want']}",
                    f"Then I should {story['benefit']}"
                ]
            }
            scenarios.append(scenario)

        return self.feature_template.render(
            feature_name="User Story Implementation",
            description="Implementation of user stories",
            scenarios=scenarios
        )

    def _generate_from_test_case(self, parsed_data: Dict[str, Any]) -> str:
        scenarios = [{
            "name": "Execute test case",
            "steps": [
                f"Given {precond}" for precond in parsed_data["preconditions"]
            ] + [
                f"When {step}" for step in parsed_data["steps"]
            ] + [
                f"Then {result}" for result in parsed_data["expected_results"]
            ]
        }]

        return self.feature_template.render(
            feature_name="Test Case Execution",
            description="Automated test case execution",
            scenarios=scenarios
        )