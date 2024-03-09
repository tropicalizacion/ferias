import pandas

table = pandas.read_csv("website_student.csv")

table.rename(columns={"id":"pk"}, inplace=True)
table = table[table["pk"].notnull()]

table_fields = table.drop(columns=["pk"])
table_fields = table_fields.transpose()
table.insert(0, "model", ["website.student" for x in range(table.shape[0])], True)
table = table[["model", "pk"]]
table["fields"] = [table_fields[i].to_dict() for i in range(table.shape[0])]

table.to_json("website_student.json", orient="records")