from langchain_community.tools.tavily_search import TavilySearchResults
from direction_indicator import direction_tool
from social_aid_tool import social_aid_tool
from qr_code_tool import qr_code_tool
from stop_tool import stop_tool
from conversation_tool import conversation_tool

##############################################################
                        # Tools #
##############################################################

#tavily_search = TavilySearchResults(max_results=2)
tools = [social_aid_tool, direction_tool, qr_code_tool, stop_tool, conversation_tool]


##############################################################