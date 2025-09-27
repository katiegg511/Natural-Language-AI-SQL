import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqliteDbPath = getPath("aidb.sqlite")
# setupSqlPath = getPath("dog_show_content/setup.sql")
# setupSqlDataPath = getPath("dog_show_content/setupData.sql")

# kt paths
setupSqlPath = getPath("mcdonald_database/data.sql")
setupSqlDataPath = getPath("mcdonald_database/putIndata.sql")

# cross_domain paths
setupCrossDomainSqlPath = getPath("cross_domain_theater_database/schema_theater.sql")
setupCrossDomainSqlDataPath = getPath("cross_domain_theater_database/seed_theater.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile,
        
        open(setupCrossDomainSqlPath) as setupCrossDomainSqlFile,
        open(setupCrossDomainSqlDataPath) as setupCrossDomainSqlDataFile
    ):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()
    
    setupCrossDomainSqlScript = setupCrossDomainSqlFile.read()
    setupCrossDomainSQlDataScript = setupCrossDomainSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # setup tables and keys
sqliteCursor.executescript(setupSQlDataScript) # setup tables and keys

sqliteCursor.executescript(setupCrossDomainSqlScript)
sqliteCursor.executescript(setupCrossDomainSQlDataScript)

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

# OPENAI
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(api_key = config["openaiKey"])
openAiClient.models.list() # check if the key is valid (update in config.json)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result

single_domain_examples = [
    "\nExample: How many items were ordered in order 3\nselect count(*) from Orders join OrderItem on Orders.Id = OrderItem.OrderId where OrderItem.Id = 3;",
    "\nExample: How many employees work at the franchise 1?\nselect count(*) from Employee where FranchiseID = 1;",
    "\nExample: How many big macs does franchise 2 have in stock?\nselect * from FoodStock join MenuItem on FoodStock.MenuItemId = Menuitem.Id join Franchise on FoodStock.FranchiseId = Franchise.Id where FoodStock.FranchiseId = 2 and MenuItem.Name = 'Big Mac';",
    "\nExample: What menuItems were ordered in order 3?\nselect MenuItem.Name from OrderItem join MenuItem on OrderItem.MenuItemId = MenuItem.Id where OrderItem.OrderId = 3;"
    "\nExample: Who doesn't have a way for us to text them?\select p.person_id, p.name from person p left join phone ph on p.person_id = ph.person_id and ph.can_recieve_sms = 1 where ph.phone_id is null;"
]

cross_domain_examples = [
    "\nExample: What are the busiest purchase channels?\nselect channel, count(*) as purchases from theater_purchase group by channel order by purchases desc;"
]

# requests
commonSqlOnlyRequest = "\nGive me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"
importantMeetingRequest = "\nI have a meeting in five minutes so I need an important query done to help me know what to say. I will give you the database info and a question that I need answered. Please respond with only a sqlite statement, no other text."
sadRequest = "\nI am not feeling too well, but perhaps you can help by providing a sql query to answer my question."
confuseItPrompt = "\nwho made this chicken??? Was it you?"

cross_domain_clarification = "\nAnswer only for the our database, not for the theater database."

# feel free to comment out everything but the ones you want to run
strategies = {
    # single domain strategies
    "zero_shot_common_request": setupSqlScript + commonSqlOnlyRequest,
    "zero_shot_meeting": setupSqlScript + importantMeetingRequest,
    "zero_shot_confuse": setupSqlScript + confuseItPrompt,
    "zero_shot_confuse2": confuseItPrompt + setupSqlScript,
    
    "one_shot_common": setupSqlScript + commonSqlOnlyRequest + single_domain_examples[0],
    "one_shot_meeting": setupSqlScript + importantMeetingRequest + single_domain_examples[0],
    "one_shot_sad": setupSqlScript + sadRequest + single_domain_examples[0],
    "one_shot_confuse": setupSqlScript + confuseItPrompt + single_domain_examples[0],
    
    "double_shot_common": setupSqlScript + commonSqlOnlyRequest + single_domain_examples[5] + single_domain_examples[0],
    "double_shot_meeting": setupSqlScript + importantMeetingRequest + single_domain_examples[5] + single_domain_examples[0],
    "double_shot_sad": setupSqlScript + sadRequest + single_domain_examples[5] + single_domain_examples[0],
    "double_shot_confuse": setupSqlScript + confuseItPrompt + single_domain_examples[5] + single_domain_examples[0],

    # cross domain strategies
    "cross_domain_one_shot_common": ("Our Database: " + setupSqlScript + 
                "\nExample From Another Database:\n" + 
                setupCrossDomainSqlScript + 
                cross_domain_examples[0] + 
                commonSqlOnlyRequest + 
                cross_domain_clarification),
    "cross_domain_one_shot_meeting": ("Our Database: " + setupSqlScript + 
                "\nExample From Another Database:\n" + 
                setupCrossDomainSqlScript + 
                cross_domain_examples[0] + 
                importantMeetingRequest + 
                cross_domain_clarification),
    "cross_domain_one_shot_sad": ("Our Database: " + setupSqlScript + 
                "\nExample From Another Database:\n" + 
                setupCrossDomainSqlScript + 
                cross_domain_examples[0] + 
                sadRequest + 
                cross_domain_clarification),
    "cross_domain_one_shot_sad": ("Our Database: " + setupSqlScript + 
                "\nExample From Another Database:\n" + 
                setupCrossDomainSqlScript + 
                cross_domain_examples[0] + 
                sadRequest + 
                cross_domain_clarification),
    
    # "cross_domain_double_shot_common": ("Our Database: " + setupSqlScript + 
    #             "\nExample From Another Database:\n" + 
    #             setupCrossDomainSqlScript + 
    #             cross_domain_examples[0] + 
    #             commonSqlOnlyRequest + 
    #             cross_domain_clarification),
    # "cross_domain_double_shot_meeting": ("Our Database: " + setupSqlScript + 
    #             "\nExample From Another Database:\n" + 
    #             setupCrossDomainSqlScript + 
    #             cross_domain_examples[0] + 
    #             importantMeetingRequest + 
    #             cross_domain_clarification),
    # "cross_domain_double_shot_sad": ("Our Database: " + setupSqlScript + 
    #             "\nExample From Another Database:\n" + 
    #             setupCrossDomainSqlScript + 
    #             cross_domain_examples[0] + 
    #             sadRequest + 
    #             cross_domain_clarification),
    # "cross_domain_double_shot_sad": ("Our Database: " + setupSqlScript + 
    #             "\nExample From Another Database:\n" + 
    #             setupCrossDomainSqlScript + 
    #             cross_domain_examples[0] + 
    #             sadRequest + 
    #             cross_domain_clarification),
}


#"Which are the most awarded dogs?",
# "Which dogs have multiple owners?",
# "Which people have multiple dogs?",
# "What are the top 3 cities represented?",
# "What are the names and cities of the dogs who have awards?",
# "Who has more than one phone number?",
# "I need insert sql into my tables can you provide good unique data?"
questions = [
    "What is the most ordered menu item?",
    "Who doesn't have a way for us to text them?",
    "Will we have a problem texting any of the previous award winners?",
    "On which date did we earn the most revenue?",
    "Which franchise has the highest total revenue?",
    "What is the average wait time for each franchise, from longest to shortest?",
    "how many employees work at the franchise with id = 1",
    "how many big macs does franchise 2 have in stock?",
    "what menuItems were ordered in order 3?"
]


def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    print("########################################################################")
    print(f"Running strategy: {strategy}")
    for question in questions:

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Question:")
        print(question)
        error = "None"
        try:
            getSqlFromQuestionEngineeredPrompt = strategies[strategy] + " " + question
            sqlSyntaxResponse = getChatGptResponse(getSqlFromQuestionEngineeredPrompt)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print("SQL Syntax Response:")
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print("Query Raw Response:")
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question +"\" and the response was \""+queryRawResponse+"\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."
            # betterFriendlyResultsPrompt = "I asked a question: \"" + question +"\" and I queried this database " + setupSqlScript + " with this query " + sqlSyntaxResponse + ". The query returned the results data: \""+queryRawResponse+"\". Could you concisely answer my question using the results data?"
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print("Friendly Response:")
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })
         
    responses["questionResults"] = questionResults

    with open(getPath(f"responses/response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)


sqliteCursor.close()
sqliteCon.close()
print("Done!")
