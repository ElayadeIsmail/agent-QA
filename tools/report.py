from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel

def write_repot(filename:str,html):
    with open(filename,"w") as f:
        f.write(html)

class WriteReportArgsSchema(BaseModel):
    filename:str
    html:str

write_report_tool = StructuredTool.from_function(
    name="write_repot",
    description="Write an html file to disc. Use this tool when ever someone asks for a report",
    func=write_repot,
    args_schema=WriteReportArgsSchema
)
