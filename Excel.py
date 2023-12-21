import pandas as pd #เพื่อใช้งาน DataFrame ของ pandas
import re #เพื่อใช้งาน Regular Expression

print("----------Welcome to My Program----------")
print("            Hope your Enjoying           ")

# รับค่าจำนวนแถวและคอลัมน์
rows = int(input("Enter number of rows (max 100): "))
cols = input("Enter number of columns (A-Z): ")
#แปลงตัวอักษร A-Z เป็นตัวเลข 1-26 เพื่อใช้ในการกำหนดจำนวนคอลัมน์
cols_num = ord(cols.upper()) - 64

if not (1 <= rows <= 100) or not (1 <= cols_num <= 26):
    print("Invalid input.")
    exit()

# สร้างตารางด้วยการสร้าง list ของ list ซึ่งจะเป็นเมทริกซ์ของค่าที่รับเข้ามา
table = []
for i in range(rows):
    row = []
    for j in range(cols_num):
        row.append(0)
    table.append(row)

# แปลงตัวอักษร A-Z เป็นตัวเลข 1-26 เพื่อใช้ในการเข้าถึง list
def column_to_number(col):
    return ord(col.upper()) - 64

# แปลงตัวเลข 1-26 เป็นตัวอักษร A-Z เพื่อใช้ในการแสดงผล
def number_to_column(num):
    return chr(num + 64)

# แสดงตาราง
def show_table():
    # สร้าง DataFrame จาก list ของ list และแปลงตัวเลขในตารางเป็นตัวอักษร A-Z ก่อน
    df = pd.DataFrame(table)
    df.columns = [number_to_column(i) for i in range(1, cols_num+1)]
    df.index = pd.RangeIndex(start=1, stop=len(df) + 1)
    print(df)


def replace_expression(expression, table):
    # หาตัวแปรในสูตรและเปลี่ยนเป็นค่าจากตาราง
    var_list = re.findall("[A-Z]\d+", expression)
    for var in var_list:
        col = var[0].upper()
        row = var[1:]
        if not row.isdigit() or not 1 <= int(row) <= rows or not 'A' <= col <= number_to_column(cols_num):
            return None
        expression = expression.replace(var, str(table[int(row)-1][column_to_number(col)-1]))
    return expression

def add_data():
    # รับค่าเซลล์และค่าจากผู้ใช้
    cell = input("Enter cell (Ex. A1): ")
    value = input("Enter value: ")

    # ตรวจสอบว่าเซลล์ที่ระบุอยู่ในช่วงที่ถูกต้องหรือไม่
    col = cell[0].upper()
    if not 'A' <= col <= number_to_column(cols_num):
        print("#ERROR#")
        return

    row = cell[1:]
    if not row.isdigit() or not 1 <= int(row) <= rows:
        print("#ERROR#")
        return

    # คำนวณค่าจากสูตร
    if "=" in value:
        try:
            # แทนค่า reference cell ด้วยค่าจากตารางและคำนวณสูตร
            for match in re.findall(r'[A-Z]+\d+', value):
                ref_cell = match
                ref_col = ref_cell[0].upper()
                ref_row = ref_cell[1:]
                if not 'A' <= ref_col <= number_to_column(cols_num) or not ref_row.isdigit() or not 1 <= int(ref_row) <= rows:
                    raise ValueError("#ERROR#")
                value = value.replace(ref_cell, str(table[int(ref_row)-1][column_to_number(ref_col)-1]))

            result = eval(value[1:], {"__builtins__": None}, {"table": table})
            table[int(row)-1][column_to_number(col)-1] = result
            print("Result: ", result)
        except ValueError as e:
            print(str(e))
            return
        except:
            print("#ERROR")
            return
    # เพิ่มหรือแทนค่าในตาราง
    else:
        if value.isdigit():
            table[int(row)-1][column_to_number(col)-1] = value
        elif value.replace('.', '').isdigit():
            table[int(row)-1][column_to_number(col)-1] = float(value)
        else:
            print("#ERROR")
            return

    # แสดงตารางออกมา
    show_table()



show_table()
while True:
    choice = input("Enter 'add' to add data or 'exit' to exit: ")
    if choice.lower() == 'add':
        add_data()
    elif choice.lower() == 'exit':
        exit()


        