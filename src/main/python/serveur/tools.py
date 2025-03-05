from langchain_community.tools.tavily_search import TavilySearchResults
from direction_indicator import direction_tool
from weather import weather_tool
from social_aid_tool import social_aid_tool
from qr_code_tool import qr_code_tool

##############################################################
                        # Tools #
##############################################################

#tavily_search = TavilySearchResults(max_results=2)
tools = [social_aid_tool, direction_tool, qr_code_tool]


##############################################################