import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import DirectoryReadTool,PDFSearchTool
from crewai_tools import SerperDevTool

tavily_tool = SerperDevTool()
os.environ["SERPER_API_KEY"] =

os.environ["TAVILY_API_KEY"] =
os.environ["OPENAI_API_KEY"] =


directory_read_tool = DirectoryReadTool(directory=r'C:\Users\Yatharth\Desktop\desktop1\AI\isro_hack\forest_fire_sample_crew\data')
tool = PDFSearchTool()

researcher = Agent(
    role='Forest Fire Management Researcher',
    goal='Extract, analyze, and compile information related to forest fire management from provided documents and online sources.',
    verbose=True,
    memory=True,
    backstory='Experienced in environmental science with a focus on forest ecosystems, you are tasked with gathering and synthesizing comprehensive data on forest fire management practices and innovations.',
    tools=[directory_read_tool, tavily_tool,tool]
)

web_research_task = Task(
    description='Conduct online research to find additional resources, case studies, and recent advancements in forest fire management.',
    expected_output='A compilation of web-based resources and recent articles and news reports that complement the information found in the provided documents.',
    tools=[tavily_tool],
    agent=researcher,
    async_execution=False,
)
directory_document_analysis_task = Task(
    description='Thoroughly review and extract key information from all PDF documents within the directory related to forest fire management, including best practices, challenges, and recommendations.',
    expected_output='A detailed summary report highlighting the main points from each document, organized by themes such as community involvement, technological innovations, and training programs.',
    tools=[directory_read_tool,tool],
    agent=researcher,
)
final_output_task = Task(
    description='Thoroughly read the information you recieve and remove all possible hallucinations and irrelevant information, transform the answer into a presentable manner',
    expected_output='A detailed summary report highlighting the main points from each document, information recieved from the web, i.e the articles , any relevant news,  technological innovations, and training programs.',
    tools=[directory_read_tool,tool],
    context = [directory_document_analysis_task, web_research_task],
    agent=researcher,
)

crew = Crew(
    agents=[researcher],
    tasks=[web_research_task,directory_document_analysis_task,final_output_task],
    process=Process.sequential
)

print("""The main points related to forest fire management as per the documents and online sources are as follows:

1. A structured system for forest fire management is crucial, considering the climate change scenario. The management of forest fires should be self-sustainable even beyond the duration of national programs.

2. Different stakeholders should be involved in forest fire management, such as the district administration, local community representatives, and private organizations.   

3. Controlled burning in protected areas is essential to prevent the accumulation of fuel load which could cause severe fires in the future.

4. A national-level awareness campaign, similar to the “Smokey Bear” campaign of the United States, may be beneficial.

5. The Joint Forest Management Committees (JFMCs) should also be part of forest fire management workshops in the future.

6. Firefighting strategies like detection and alert systems are being implemented, with specific focus on vulnerable districts for increased fire preparedness.

Advancements in Forest Fire Management:

1. Remote sensing techniques are being used for real-time data on fire hotspots, smoke plumes, and burned areas.

2. Cutting-edge technologies such as supercomputers generating near-real-time fire maps and drones are being employed.

3. The integration of Internet of Things (IoT) and Artificial Intelligence (AI) capabilities is suggested for improving forest fire detection and mitigation tactics.      

Case Studies and Strategies in Forest Fire Management:

1. Land managers globally are integrating diverse societal goals with fire and forest management.

2. The National Cohesive Wildland Fire Management Strategy (NCWFMS) and the U.S. Forest Service's "Confronting the Wildfire Crisis: A Strategy for Protecting Communities and Improving Resilience in America's Forests" are examples of strategies being implemented.

3. Lessons learned from wildland fire case studies in forests of the western United States and Great Lakes region are being used to reform forest fire management.
      """)
# Execute the crew

result = crew.kickoff(inputs={'data_directory':r"C:\Users\Yatharth\Desktop\desktop1\AI\isro_hack\forest_fire_sample_crew\data"})
