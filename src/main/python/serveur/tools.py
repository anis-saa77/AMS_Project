from langchain_community.tools.tavily_search import TavilySearchResults
from schedule import ScheduleTool
from direction_indicator import DiretionIndicationTool
from social_aid import SocialAidTool
from weather import check_weather

##############################################################
                        # Tools #
##############################################################


tavily_search = TavilySearchResults(max_results=2)
schedule = ScheduleTool()
dir = DiretionIndicationTool()
social_aid = SocialAidTool()
#search de greg
tools = [check_weather]


##############################################################