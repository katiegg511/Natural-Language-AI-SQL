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
# setupSqlPath = getPath("setup.sql")
# setupSqlDataPath = getPath("setupData.sql")

# new paths with fastfood data
setupSqlPath = getPath("data.sql")
setupSqlDataPath = getPath("putIndata.sql")


# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile
    ):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # setup tables and keys
sqliteCursor.executescript(setupSQlDataScript) # setup tables and keys

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
    "Example: how many items were ordered in order 3\nselect count(*) from Orders join OrderItem on Orders.Id = OrderItem.OrderId where OrderItem.Id = 3;",
    "Example: how many employees work at the franchise 1?\nselect count(*) from Employee where FranchiseID = 1;",
    "Example: how many big macs does franchise 2 have in stock?\nselect * from FoodStock join MenuItem on FoodStock.MenuItemId = Menuitem.Id join Franchise on FoodStock.FranchiseId = Franchise.Id where FoodStock.FranchiseId = 2 and MenuItem.Name = 'Big Mac';",
    "Example: what menuItems were ordered in order 3?\nselect MenuItem.Name from OrderItem join MenuItem on OrderItem.MenuItemId = MenuItem.Id where OrderItem.OrderId = 3;"
]

cross_domain_examples = [
    "who doesn't have a way for us to text them?\nselect p.person_id, p.name\nfrom person p\nleft join phone ph on p.person_id = ph.person_id and ph.can_recieve_sms = 1\nwhere ph.phone_id is null;\n"
]

# strategies
commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"
importantMeetingRequest = "I have a meeting in five minutes so I need an important query done to help me know what to say. I will give you the database info and a question that I need answered. Please respond with only a sqlite statement, no other text."
sadRequest = "I am not feeling too well, but perhaps you can help by providing a sql query to answer my question."
confuseItPrompt = "who made this chicken??? Was it you?"

# feel free to comment out everything but the ones you want to run
strategies = {
    # example strategies here
    # "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    # "single_domain_double_shot": (setupSqlScript +
    #                " Who doesn't have a way for us to text them? " +
    #                " \nSELECT p.person_id, p.name\nFROM person p\nLEFT JOIN phone ph ON p.person_id = ph.person_id AND ph.can_recieve_sms = 1\nWHERE ph.phone_id IS NULL;\n " +
    #                commonSqlOnlyRequest),

    # our groups strategies 
    # "zero_shot_meeting": setupSqlScript + importantMeetingRequest,
    # "single_domain_one_shot": setupSqlScript + importantMeetingRequest + single_domain_examples[0],
    # "single_domain_one_shot2": setupSqlScript + sadRequest + single_domain_examples[0],
    # "single_domain_one_shot3": setupSqlScript + sadRequest + single_domain_examples[0],
    "single_domain_confuse_zero_shot": setupSqlScript + confuseItPrompt,
    "single_domain_confuse2_zero_shot": confuseItPrompt + setupSqlScript
}

questions = [
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

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)


sqliteCursor.close()
sqliteCon.close()
print("Done!")
