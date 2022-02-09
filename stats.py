from requests import get
import json

# Change the url depending on which platform you want to test
# Desktop               https://privacytests.org/index.json
# Desktop private       https://privacytests.org/private.json
# iOS                   https://privacytests.org/ios.json
# Android               https://privacytests.org/android.json
# Nightly               https://privacytests.org/nightly.json
# Nightly private       https://privacytests.org/nightly-private.json
url = "https://privacytests.org/index.json"

data: dict = json.loads(get(url).text)

browsers: list[dict] = data["all_tests"]
rankings = {}

for browser in browsers:
    browserName = browser["browser"]
    if browserName not in rankings.keys():
        rankings[browserName] = 0
    if browser["testResults"] == None:
        continue
    for topicName in browser["testResults"].keys():
        for testName in browser["testResults"][topicName].keys():
            if "passed" in browser["testResults"][topicName][testName].keys():
                if browser["testResults"][topicName][testName]["passed"]:
                    rankings[browserName] += 1
            elif "testFailed" in browser["testResults"][topicName][testName].keys():
                if not browser["testResults"][topicName][testName]["testFailed"]:
                    rankings[browserName] += 1

nameLength = max([len(a) for a in rankings.keys()]) + 2
bestPoints = max(list(rankings.values()))
rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
for name, points in rankings:
    starCount = round(points * 100 / bestPoints)
    print(f"{name:{nameLength}} {'*'*starCount} {' '*(100-starCount)} {points:3}")
