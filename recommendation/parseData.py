
data = [
    
    {
        "id":1,
        "age":15,
        "IQ":45.5,
        "arm":"Science",
        "subjects" : {
            "Mathematics": 4,
            "Chemistry" : 5,
            "Biology": 4,
            "Physics" : 3
        }  
        
    },
    {
        "id":2,
        "age":15,
        "IQ":45.5,
        "arm":"Art",
        "subjects" : {
            "Mathematics": 4,
            "History" : 5,
            "CRK": 4,
            "Lit-English" : 3,
            "Government" : 2
        }
        
        
    },
    {
        "id":3,
        "age":15,
        "IQ":45.5,
        "arm":"Commercial",
        "subjects" : {
            "Mathematics": 4,
            "Accounting" : 5,
            "Economics": 4,
            "Commerce" : 3
        }
        
        
    }
]


dataform = []
science_padding = [0,0,0,0,0,0,0]
print(dataform.insert(0,science_padding))

formata = ['AGE','IQ', 'MATHEMATICS',
       'BIOLOGY', 'PHYSICS', 'CHEMISTRY', 'ACCOUNTING', 'COMMERCE',
       'ECONOMICS', 'GOVERNMENT', 'LIT-IN-ENG', 'HISTORY', 'CRK']

for entry in data:
    if entry["arm"] == "Science":
        dataform = [entry["arm"], entry["IQ"]]
        for subj in entry["subjects"]:
            dataform = [entry["subjects"]["Mathematics"],entry["subjects"]["Biology"],entry["subjects"]["Physics"],entry["subjects"]["Chemistry"] ]+science_padding
        print(dataform)
    elif entry["arm"] == "Art":
        dataform = [entry["arm"], entry["IQ"]]
        for subj in entry["subjects"]:
            dataform = [entry["subjects"]["Mathematics"],0,0,0,0,0,0,entry["subjects"]["Government"],entry["subjects"]["Lit-English"],entry["subjects"]["History"],entry["subjects"]["CRK"]]
        
        print(dataform)
        
    elif entry["arm"] == "Commercial":
        dataform = [entry["arm"], entry["IQ"]]
        for subj in entry["subjects"]:
            dataform = [entry["subjects"]["Mathematics"],0,0,0,entry["subjects"]["Accounting"],entry["subjects"]["Commerce"],entry["subjects"]["Economics"],0,0,0,0]
        
        print(dataform)


# padding = [0,0,0,0]
# data = []
