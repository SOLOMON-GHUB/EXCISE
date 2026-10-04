age = int(input("请输入你的年龄："))

print("参赛资格审核如下：")
if 18 <= age <= 45:  # 等价于age >= 18 and age <= 45
    print("年龄符合参赛要求！")

    report = input("是否提交了体检报告？（是/否）")
    if report == "是":
        print("已经提交体检报告，可以参赛!")

        level = int(input("请输入你的会员等级：（1/2/3）"))
        if level == 1:
            print(f"你是{level}级会员，比赛结束可已领取纪念T恤一件！")
        elif level ==2:
            print(f"你是{level}比赛结束可已领取跑鞋一双！")
        elif level == 3:
            print(f"你是{level}比赛结束可已领取运动耳机一付！")
        else:
            print("输入的会员等级不对！")  # 这个else可以不写

    elif report == "否":
        print("未提交体检报告，不可以参赛!")
    else:
        print("没有提交体检报告！！！")
else:
    print("NO PASS!")
    exit()