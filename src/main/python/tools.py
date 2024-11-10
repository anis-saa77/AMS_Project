from langchain_community.tools.tavily_search import TavilySearchResults

##############################################################
                        # Tools #
##############################################################


search = TavilySearchResults(max_results=2)
tools = [search]


##############################################################