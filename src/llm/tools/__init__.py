from llm.tools.architecture import architecture_advisor
from llm.tools.performance import performance_diagnoser
from llm.tools.principles import solid_principles_advisor
from llm.tools.profile import runtime_profile_reader
from llm.tools.review import code_review_checklist_builder

MOBILE_EXPERT_TOOLS = [
    runtime_profile_reader,
    architecture_advisor,
    performance_diagnoser,
    solid_principles_advisor,
    code_review_checklist_builder,
]
