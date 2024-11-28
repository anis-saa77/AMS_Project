from langchain_community.tools.tavily_search import TavilySearchResults
from schedule import ScheduleTool
from direction_indicator import DiretionIndicationTool
from social_aid import SocialAidTool

##############################################################
                        # Tools #
##############################################################


search = TavilySearchResults(max_results=2)
schedule = ScheduleTool()
dir = DiretionIndicationTool()
social_aid = SocialAidTool
tools = [search, schedule, dir, social_aid]


##############################################################