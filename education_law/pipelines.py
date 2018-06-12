import pymysql
def dbHandle():
    conn = pymysql.connect(
        host="localhost",
        user ="root",
        passwd = "1234567890",
        charset = "utf8",
        use_unicode = False
    )
    return conn
class EducationLawPipline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE education_law")  # education_lawjianshu
        sql = "INSERT INTO articles(PublishingUnits,Title,PublishTime,ArticleUrl ,CrawlTime,Area,Heat,Classification,Annex,Content) VALUES( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s )"
        try:
            cursor.execute(sql, (item['PublishingUnits'], item['Title'], item['PublishTime'], item['ArticleUrl'] , item['CrawlTime'] , item['Area'], item['Heat'], item['Classification'], item['Annex'], item['Content']))
            cursor.connection.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
            dbObject.rollback()
        return item
