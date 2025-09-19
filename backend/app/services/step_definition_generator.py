from typing import Dict, Any, List
import jinja2
from pathlib import Path

class StepDefinitionGenerator:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate_step_definitions(
        self,
        feature_content: str,
        programming_language: str,
        framework: str = None
    ) -> Dict[str, Any]:
        """Generate step definitions for the given feature file content."""
        # Extract steps from feature content
        steps = self._extract_steps(feature_content)
        
        # Generate step definitions based on language and framework
        if programming_language.lower() == "python":
            return self._generate_python_steps(steps, framework or "behave")
        elif programming_language.lower() == "javascript":
            return self._generate_javascript_steps(steps, framework or "cucumber")
        else:
            raise ValueError(f"Unsupported programming language: {programming_language}")

    def _extract_steps(self, feature_content: str) -> List[Dict[str, str]]:
        """Extract steps from feature file content."""
        steps = []
        lines = feature_content.split("\n")
        
        for line in lines:
            line = line.strip()
            if line.startswith(("Given ", "When ", "Then ", "And ", "But ")):
                keyword = line.split()[0]
                step_text = " ".join(line.split()[1:])
                steps.append({
                    "keyword": keyword,
                    "text": step_text
                })
        
        return steps

    def _generate_python_steps(self, steps: List[Dict[str, str]], framework: str) -> Dict[str, Any]:
        """Generate Python step definitions."""
        template = self.env.get_template("python_steps.py.jinja")
        
        # Convert step text to function names and patterns
        step_implementations = {}
        for step in steps:
            func_name = self._create_function_name(step["text"])
            pattern = self._create_step_pattern(step["text"])
            step_implementations[pattern] = func_name

        return {
            "step_definitions": template.render(
                steps=step_implementations,
                framework=framework
            ),
            "imports": [
                "from behave import given, when, then",
                "from hamcrest import assert_that, equal_to"
            ]
        }

    def _generate_javascript_steps(self, steps: List[Dict[str, str]], framework: str) -> Dict[str, Any]:
        """Generate JavaScript step definitions."""
        template = self.env.get_template("javascript_steps.js.jinja")
        
        # Convert step text to function names and patterns
        step_implementations = {}
        for step in steps:
            func_name = self._create_function_name(step["text"])
            pattern = self._create_step_pattern(step["text"])
            step_implementations[pattern] = func_name

        return {
            "step_definitions": template.render(
                steps=step_implementations,
                framework=framework
            ),
            "imports": [
                "const { Given, When, Then } = require('@cucumber/cucumber');",
                "const { expect } = require('chai');"
            ]
        }

    def _create_function_name(self, step_text: str) -> str:
        """Convert step text to a valid function name."""
        # Remove special characters and convert to snake_case
        name = "".join(c.lower() if c.isalnum() else "_" for c in step_text)
        return "_".join(word for word in name.split("_") if word)

    def _create_step_pattern(self, step_text: str) -> str:
        """Convert step text to a regex pattern."""
        # Replace numbers and quoted strings with capture groups
        pattern = step_text
        pattern = re.sub(r'\d+', r'(\d+)', pattern)
        pattern = re.sub(r'"([^"]*)"', r'"([^"]*)"', pattern)
        return f"^{pattern}$"