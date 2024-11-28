from langchain_community.tools.tavily_search import TavilySearchResults
from schedule import ScheduleTool
from direction_indicator import DiretionIndicationTool
from social_aid import SocialAidTool

##############################################################
                        # Tools #
##############################################################


tavily_search = TavilySearchResults(max_results=2)
schedule = ScheduleTool()
dir = DiretionIndicationTool()
social_aid = SocialAidTool()
#search de greg
tools = [tavily_search, schedule]


##############################################################