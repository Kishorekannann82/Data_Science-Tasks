from semantic_kernel import Kernel
from tools.csv_plugin import CSVPlugin
from tools.email_plugin import EmailPlugin
from tools.insight_plugin import InsightPlugin
from tools.memory_plugin import MemoryPlugin
class AutonomousTaskAgent:
    def __init__(self):
        self.kernel = Kernel()

        self.csv_plugin = CSVPlugin()
        self.email_plugin = EmailPlugin()
        self.insight_plugin = InsightPlugin()
        self.memory_plugin = MemoryPlugin()

        self.kernel.add_plugin(self.csv_plugin, plugin_name="csv_plugin")
        self.kernel.add_plugin(self.insight_plugin, plugin_name="insight_plugin")
        self.kernel.add_plugin(self.email_plugin, plugin_name="email_plugin")
        self.kernel.add_plugin(self.memory_plugin, plugin_name="memory_plugin")

    def run(self, task: str, file_path: str) -> dict:
        csv_result = self.csv_plugin.analyze_csv(file_path)
        csv_text_summary = csv_result["text_summary"]
        insights = self.insight_plugin.generate_insights(csv_text_summary)
        email_draft = self.email_plugin.create_email_draft(insights)
        memory_status = self.memory_plugin.save_memory(
            task=task,
            csv_summary=csv_text_summary,
            insights=insights,
            email_draft=email_draft
        )
        return {
            "task": task,
            "csv_result": csv_result,
            "insights": insights,
            "email_draft": email_draft,
            "memory_status": memory_status
        }
    def get_memory(self) -> str:
        return self.memory_plugin.load_memory()