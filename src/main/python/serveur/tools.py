from langchain_community.tools.tavily_search import TavilySearchResults
from schedule import ScheduleTool
from direction_indicator import DiretionIndicationTool
from social_aid import SocialAidTool
from weather import weather_tool
from social_aid_tool import social_aid_tool


##############################################################
                        # Tools #
##############################################################


tavily_search = TavilySearchResults(max_results=2)
schedule = ScheduleTool()
dir = DiretionIndicationTool()

tools = [social_aid_tool, schedule, dir]


##############################################################