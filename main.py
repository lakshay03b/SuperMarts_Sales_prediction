from flask import Flask,render_template,request
from flask_cors import cross_origin
import pickle
from datetime import date
app=Flask(__name__)


with open("rf_model.pkl","rb") as model_file:
    model=pickle.load(model_file)

@app.route('/')
@cross_origin()
def  index():
    return render_template('home.html')
@app.route("predict",methods=['GET','POST'])
@cross_origin()
def predict():
    if request.method=="POST":
        output=0
        Item_Weight=float(request.form['Item_Weight'])
        item_fat_content=request.form['Item_Fat_Content']
        Item_visibility=float(request.form['Item_Visibility'])
        item_type=request.form['Item_Type']
        item_mrp=float(request.form['Item_MRP'])
        outlet_establishment_year=int(request.form['Outlet_Establishment_Year'])
        outlet_size=request.form['Outlet_Size']
        outlet_Location_Type=request.form['Outlet_Location_Type']
        outlet_type=request.form['Outlet_Type']
        
        todays_date=date.today()
        Outlet_years=todays_date.year-outlet_establishment_year
        
        Item_Visibility_MeanRatio=1.06
        item_fat_content_0=0
        item_fat_content_1=0
        item_fat_content_2=0
        
        if item_fat_content=="Low Fat":
            item_fat_content_0=1
        elif item_fat_content=="Non-Edible":
            item_fat_content_1=1
        else:
            item_fat_content_2=1
        
        outlet_size_0=0
        outlet_size_1=0
        outlet_size_2=0
        
        if outlet_size=="High":
            outlet_size_0=1
        elif outlet_size=="Medium":
            outlet_size_1=1
        else:
            oultet_size2=1
        
        outlet_location_type_0=0
        outlet_location_type_1=0
        outlet_location_type_2=0
        
        if outlet_Location_Type=="Tier 1":
            outlet_location_type_0=1
        elif outlet_Location_Type=="Tier 2":    
            outlet_location_type_1=1
        else:
            outlet_location_type_2=1
        
        outlet_type_0=0
        outlet_type_1=0
        outlet_type_2=0
        outlet_type_3=0
        
        if outlet_type=="Grocery Store":
            outlet_type_0=1
        elif outlet_type=="Supermarket Type1":
            outlet_type_1=1
        elif outlet_type=="Supermarket Type2":
            outlet_size_2=1
        else:
            outlet_size_3=1
            
        item_type_0=0
        item_type_1=0
        item_type_2=0
        
        if item_type=="Drinks":
            item_type_0=1
        elif item_type=="Food":
            item_type_1=1
        else:
            item_type_2=1
        
        feature=[Item_Weight,Item_visibility,item_mrp,Outlet_years,Item_Visibility_MeanRatio,
                 item_fat_content_0,item_fat_content_1,item_fat_content_2,outlet_size_0,outlet_size_1,
                 outlet_size_2,outlet_location_type_0,outlet_location_type_1,outlet_location_type_2,
                 outlet_type_0,outlet_type_1,outlet_type_2,outlet_type_3,item_type_0,item_type_1,
                 item_type_2]
        try:
            result=model.predict([feature])[0]
            print(result)
            render_template('home.html',result)
            
        except:
            print("Error")
    return render_template('home.html')
            
if __name__ == '__main__':
    app.run(debug=True)
    