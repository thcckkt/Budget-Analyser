import csv,decimal,datetime,os#引入csv,decimal,datetime,os库
listexpense=[ ]#创建总体的listexpense列表
past_expenses=set()#创建一个past_expense元组为查重准备
filename='expense.csv'#为文件设置变量
if os.path.exists(filename) and os.path.getsize(filename) >0:#检测文件存在并不为空  
    with open(filename,'r',encoding='utf-8') as file:#打开文件
        for row in csv.DictReader(file):#读取每一列
            try:
            #读取到的内容添加到dictexpense字典
                dictexpense={
                "amount": decimal.Decimal(row["amount"]),
                "category": row["category"],
                "date": row["date"]
                }
                #把数据添加到past_expense元组便于查重
                current_expense=(dictexpense["amount"],dictexpense["category"],dictexpense["date"])
                past_expenses.add(current_expense)
                #将dictexpense字典添加到listexpense列表
                listexpense.append(dictexpense)
                
            #检测有没有问题
            except (ValueError,KeyError,decimal.InvalidOperation):
                print(f'warning: invalid date, {row} has been skiped')
                continue

#备注：后期做可视化界面时考虑把错误数据呈现给用户

all_amount=decimal.Decimal('0')#初始化总金额
while True:
    amount_str=input("Enter the amount or enter 'q' to exit")#获取金额或退出
    #检查是否退出
    if amount_str.lower()=='q':
        print('Record finshed')
        #打开文件准备写入
        with open(filename,'w',encoding='utf-8',newline='') as file:
            filenames=["amount","category","date"]#定义表头
            writer=csv.DictWriter(file,filenames=filenames)#把文件变为变量用于写入
            writer.writeheader()#打包表头
            #把listexpense列表的数据保存到文件中
            for item in listexpense:
                writer.writerow({
                    "amount": str(item["amount"]),
                    "category": item["category"],
                    "date": item["date"]
                })
        break
    #获取金额(正数)
    try:
        amount=decimal.Decimal(amount_str)
    except ValueError:
        print("Amount must be number! Please try again.")
        continue
    if amount<=0:
        print("Amount must be greater than 0! Please try again.")
        continue    
    #获取类别(不能是空字符)
    category=str(input("Enter the category: "))
    if not category.strip():
        print("Category cannot be empty! Please try again.")
        continue
    #获取日期(合法格式)
    date=input("Enter the date (YYYY-MM-DD): ")
    try:
        datetime.datetime.strptime(date,"%Y-%m-%d")
    except ValueError:
        print("Date must be YYYY-MM-DD! Please try again.")
        continue
    #添加数据进入dictexpense字典
    dictexpense={
        "amount": amount,
        "category": category,
        "date": date
    }
    current_expense=(amount,category,date)
    if current_expense in past_expenses:
        print("Expense exists! Please try again")
        continue
    else:
        past_expenses.add(current_expense)#保存这次的数据到past_expense元组中
        #添加数据进入listexpense列表
        listexpense.append(dictexpense)
        print("Record success!\n")
all_categories={}#创建all_categories字典用于存放单个类别的总金额
#获取总金额和单个类别的金额
for dictexpense in listexpense:    
    all_amount+=dictexpense["amount"]#获取总金额
    #将dictexpense内的category下的值读取并累加到all_categories的category内
    all_categories[dictexpense["category"]]=all_categories.get(dictexpense["category"],decimal.Decimal('0'))+dictexpense["amount"]
#输出总金额
print(f"total amount: {all_amount} ")
#输出单个类别的金额
for k,v in all_categories.items():
    print(f"category:{k},amount{v}")
#获取平均金额并输出
if len(listexpense)>0:
    ave_amount=all_amount/len(listexpense)
    print(f'average amount:{ave_amount}')