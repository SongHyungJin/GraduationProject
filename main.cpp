#include <iostream>
#include <cstdio>
#include <list>
#include <vector>
#include <tuple>
#include <string>
#include <cmath>
#define INPUT_FILE_NAME "input.txt"
#define OUTPUT_FILE_NAME "output.txt"
using namespace std;
void doTask();
void join();
void withdrawal();
void login();
void logout();
void addSellingProduct();
void addProduct();
void showSellingProduct();
void showSoldOutProduct();
void searchProduct();
void purchase();
void showHistory();
void writeSatisfaction();
void showStatics();
class Join;
FILE* in_fp, *out_fp;
struct Detail{
    string productName;
    string productCompany;
    int price;
} Detail_;
class Product{
private:
    Detail productDetail;
    float satisfaction;
    int reviewNum;
    int stock;
    int soldCount;
    string sellerID;
public:
    Product(Detail det, float satisfaction, int reviewNum, int stock, string sellerID){
        productDetail=det;
        this->satisfaction=satisfaction;
        this->reviewNum=reviewNum;
        this->stock=stock;
        this->soldCount=0;
        this->sellerID=sellerID;
    }
    Detail getProductDetail(){
        return this->productDetail;
    }
    bool writeSatisfaction(int review){
        satisfaction=(satisfaction*reviewNum+review)/(reviewNum+1);
        this->reviewNum++;
        return true;
    }
    float getProductSatisfaction(){
        return satisfaction;
    }
    int getStock(){
        return stock;
    }
    int getSoldCount(){
        return soldCount;
    }
    string getSellerID(){
        return sellerID;
    }
    vector<string> productSold(){
        this->stock--;
        this->soldCount++;
        vector<string> temp;
        temp.push_back(sellerID);
        temp.push_back(productDetail.productName);
        return temp;
    }
    tuple<string,int,float> getStat(){
        return make_tuple(productDetail.productName,productDetail.price*soldCount,satisfaction);
    }
};
list<Product *> productList;
class User{
private:
    string name;
    string IDnumber;
    string ID;
    string password;
    list<Product *> sellingProductList;
    list<Product *> boughtProductList;
public:
    User(string name, string IDnumber, string ID, string password){
        this->name=name;
        this->IDnumber=IDnumber;
        this->ID=ID;
        this->password=password;
    }
    bool checkInfo(string ID, string password){
        return this->ID==ID && this->password==password;
    }
    string getID(){
        return this->ID;
    }
        vector<tuple<Detail,int>> sendSellingProduct(){
        vector<tuple<Detail,int>> temp;
        for(Product* pro:sellingProductList){
            if(pro->getStock()>0){
                Detail det = pro->getProductDetail();
                temp.push_back(tuple<Detail,int>(det,pro->getStock()));
            }
        }
        return temp;
    }
    vector<tuple<Detail,int,float>> sendSoldOutProduct(){
        vector<tuple<Detail,int,float>> temp;
        for(Product* pro:sellingProductList){
            if(pro->getStock()>0){
                Detail det = pro->getProductDetail();
                temp.push_back(tuple<Detail,int,float>(det,pro->getStock(),pro->getProductSatisfaction()));
            }
        }
        return temp;
    }
    
    vector<tuple<Detail,int,float>> sendBoughtProduct(){
        vector<tuple<Detail,int,float>> temp;
        for(Product* pro:boughtProductList){
            Detail det = pro->getProductDetail();
            temp.push_back(tuple<Detail,int,float>(det,pro->getStock(),pro->getProductSatisfaction()));
        }
        return temp;
    }
    
    void addNewProduct(string proName, string productCompany, int price, int stock){
        struct Detail det = {proName, productCompany, price};
        Product *pro = new Product(det,0,0,stock,this->getID());
        sellingProductList.push_back(pro);
        productList.push_back(pro);
    }
    void addBoughtList(Product *pro){
        boughtProductList.push_back(pro);
    }
    vector<tuple<string,int,float>> getSoldStat(){
        vector<tuple<string,int,float>> temp;
        for(Product *pro:sellingProductList){
            temp.push_back(pro->getStat());
        }
        return temp;
    }
};
list<User> userList;
User *currentUser;
Product *selectedProduct;
class UserList{
private:
    list<User> userList;
public:
    void addNewUser(User user){
        userList.push_back(user);
    }
    bool deleteUser(){
        for (auto it = userList.begin(); it != userList.end(); it++) {
            if (it->getID() == currentUser->getID()) {
                userList.erase(it);
                return true;
            }
        }
        return false;
    }
    bool checkInfo(string ID, string password){
        for(auto it = userList.begin();it!=userList.end();it++){
            if(it->checkInfo(ID, password)){
                currentUser=&(*it);
                return true;
            }
        }
        return false;
    }
    
};
UserList *UserControl=new UserList();



class JoinUI{
private:
    char name[255];
    char IDnumber[255];
    char ID[255];
    char password[255];
public:
    void startInterface(){
        fprintf(out_fp,"1.1 회원가입\n");
    }
    vector<char*> inputInfo(){
        fscanf(in_fp, "%s %s %s %s\n",name,IDnumber,ID,password);
        vector<char*> temp;
        temp.push_back(name);
        temp.push_back(IDnumber);
        temp.push_back(ID);
        temp.push_back(password);
        return temp;
    }
    void write(){
        fprintf(out_fp,"> %s %s %s %s\n\n",name,IDnumber,ID,password);
    }
};

class Join{
private:
    string name;
    string IDnumber;
    string ID;
    string password;
    JoinUI* UI;
public:
    Join(){
        UI = new JoinUI();
        UI->startInterface();
        getInfo(UI->inputInfo());
        UserControl->addNewUser(*makeUser());
        UI->write();
    }
    void getInfo(vector<char*> info){
        name = info[0];
        IDnumber = info[1];
        ID = info[2];
        password = info[3];
    }
    User* makeUser(){
        User* us = new User(name, IDnumber, ID,password);
        return us;
    }
};

class WithdrawalUI {
private:
    char ID[255];
public:
    void startInterface() {
        fprintf(out_fp, "1.2 회원탈퇴\n");
    }
    void write() {
        fprintf(out_fp, "> %s \n\n", ID);
    }
};
class Withdrawal {
private:
    string ID;
    WithdrawalUI* UI;
public:
    Withdrawal() {
        UI = new WithdrawalUI();
        UI->startInterface();
        if (UserControl->deleteUser())
            UI->write();
    }
};

class LoginUI {
private:
    char ID[255];
    char password[255];
public:
    void startInterface() {
        fprintf(out_fp, "2.1 로그인\n");
    }
    vector<char*> inputInfo() {
        fscanf(in_fp, "%s %s \n", ID, password);
        vector<char*> temp;
        temp.push_back(ID);
        temp.push_back(password);
        return temp;
    }
    void write() {
        fprintf(out_fp, "> %s %s \n\n", ID, password);
    }
};

class Login {
private:
    string ID;
    string password;
    LoginUI* UI;
public:
    Login() {
        UI = new LoginUI();
        UI->startInterface();
        getInfo(UI->inputInfo());
        if (UserControl->checkInfo(ID, password))   UI->write();
    }
    void getInfo(vector<char*> info){
        ID = info[0];
        password = info[1];
    }

};


class LogoutUI {
private:
    string ID;
public:
    void startInterface() {
        fprintf(out_fp, "2.2. 로그아웃\n");
    }
    void write() {
        fprintf(out_fp, "> %s \n\n", currentUser->getID().c_str());
    }
};

class Logout {
private:
    string ID;
    LogoutUI* UI;
public:
    Logout() {
        UI = new LogoutUI();
        UI->startInterface();
        UI->write();
        currentUser=NULL;
    }
};

class AddSellingProductUI {
private:
    char productName[255];
    char productCompany[255];
    int price;
    int stock;
public:
    void startInterface() {
        fprintf(out_fp, "3.1. 판매의류등록\n");
    }
    vector<char*> inputProductInfo() {
        fscanf(in_fp, "%s %s ", productName, productCompany );
        vector<char*> temp;
        temp.push_back(productName);
        temp.push_back(productCompany);
        return temp;
    }
    vector<int> inputProductInfo2() {
        fscanf(in_fp, "%d %d\n",  &price, &stock);
        vector<int> temp;
        temp.push_back(price);
        temp.push_back(stock);
        return temp;
    }
    void write() {
        fprintf(out_fp, "> ");
        fprintf(out_fp, "%s %s %d %d\n\n", productName, productCompany, price, stock);
    }

};
class AddSellingProduct {
private:
    string productName;
    string productCompany;
    int price;
    int stock;
    AddSellingProductUI* UI;
public:
    AddSellingProduct() {
        UI = new AddSellingProductUI();
        UI->startInterface();
        getProductInfo(UI->inputProductInfo(), UI->inputProductInfo2());
        currentUser->addNewProduct(productName,productCompany,price,stock);
        UI->write();
    }
    void getProductInfo(vector<char*>info, vector<int>info2)
    {
        productName=info[0];
        productCompany=info[1];
        price=info2[0];
        stock=info2[1];
    }
};



class ShowSellingProductUI {
private:

public:
    void startInterface() {
        fprintf(out_fp, "3.2. 등록상품조회\n");
    }
    void write(vector<tuple<Detail,int>> info){
        fprintf(out_fp, "> ");
        for(auto it=info.begin();it!=info.end();it++){
            fprintf(out_fp,"%s %s %d %d\n",get<0>(*it).productName
                    .c_str(),get<0>(*it).productCompany
                    .c_str(),get<0>(*it).price,get<1>(*it));
        }
        fprintf(out_fp, "\n");;

    }

};
class ShowSellingProduct {
private:
    ShowSellingProductUI* UI;
public:
    ShowSellingProduct() {
        UI = new ShowSellingProductUI();
        UI->startInterface();
        UI->write(currentUser->sendSellingProduct());
    }

};


class ShowSoldOutProductUI {
private:

public:
    void startInterface() {
        fprintf(out_fp, "3.3. 판매완료상품조회\n");
    }
    void write(vector<tuple<Detail,int,float>> info){
        fprintf(out_fp,"> ");
        for(auto it=info.begin();it!=info.end();it++){
            fprintf(out_fp,"%s %s %d %d %d\n",get<0>(*it).productName
                    .c_str(),get<0>(*it).productCompany
                    .c_str(),get<0>(*it).price,get<1>(*it),lround(get<2>(*it)));
        }
        fprintf(out_fp, "\n");
    }
};
class ShowSoldOutProduct {
private:
    ShowSoldOutProductUI* UI;
public:
    ShowSoldOutProduct() {
        UI = new ShowSoldOutProductUI();
        UI->startInterface();
        UI->write(currentUser->sendSoldOutProduct());
    }
};


class SearchProductUI {
private:
    char productName[255];
public:
    void startInterface() {
        fprintf(out_fp, "4.1. 상품정보검색\n");
    }
    string inputProductName() {
        fscanf(in_fp, "%s\n", productName);
        return productName;
    }
    void write(Product* pro){
        Detail det = pro->getProductDetail();
        if(det.productName==productName){
            selectedProduct=pro;
            fprintf(out_fp,"> %s %s %s %d %d %d\n\n",pro->getSellerID().c_str(),det.productName.c_str(),det.productCompany.c_str(),det.price,pro->getStock(),lround(pro->getProductSatisfaction()));
        }
    }
};
class SearchProduct {
private:
    string productName;
    SearchProductUI* UI;
public:
    SearchProduct() {
        UI = new SearchProductUI();
        UI->startInterface();
        getProductName(UI->inputProductName());
        for(Product* pro:productList){
            UI->write(pro);
        }
    }
    void getProductName(string info) {
        productName=info;
    }

};


class PurchaseUI {
private:

public:
    void startInterface() {
        fprintf(out_fp, "4.2. 상품구매\n");
    }
    void write(vector<string> info){
        fprintf(out_fp,"> %s %s\n\n",info[0].c_str(),info[1].c_str());
    }


};
class Purchase {
private:
    PurchaseUI* UI;
public:
    Purchase() {
        UI = new PurchaseUI();
        UI->startInterface();
        UI->write(selectedProduct->productSold());
        currentUser->addBoughtList(selectedProduct);
    }


};



class ShowHistoryUI {
private:

public:
    void startInterface() {
        fprintf(out_fp, "4.3. 상품구매내역조회\n");
    }
    void write(vector<tuple<Detail,int,float>> info){
        fprintf(out_fp, "> ");
        for(auto it=info.begin();it!=info.end();it++)
            fprintf(out_fp,"%s %s %d %d %d\n",get<0>(*it).productName.c_str(),get<0>(*it).productCompany.c_str(),get<0>(*it).price,get<1>(*it),lround(get<2>(*it)));
        fprintf(out_fp, "\n");
    }
};
class ShowHistory {
private:
    ShowHistoryUI* UI;
public:
    ShowHistory() {
        UI = new ShowHistoryUI();
        UI->startInterface();
        UI->write(currentUser->sendBoughtProduct());
    }

};

class WriteSatisfactionUI {
private:
    char ProductName[255];
    int satisfyNum;
public:
    void startInterface() {
        fprintf(out_fp, "4.4. 상품 구매만족도 평가\n");
    }
    tuple<string,int> inputInfo() {
        fscanf(in_fp, "%s %d\n", ProductName, &satisfyNum);
        return make_tuple(ProductName,satisfyNum);
    }
    void write(tuple<string,string,float> temp){
        fprintf(out_fp, "> %s %s %d\n\n", get<0>(temp).c_str(), get<1>(temp).c_str(), lround(get<2>(temp)));
    }
};
class WriteSatisfaction {
private:
    WriteSatisfactionUI* UI;
public:
    WriteSatisfaction() {
        UI = new WriteSatisfactionUI();
        UI->startInterface();
        tuple<string,string,float> temp = inputInfo(UI->inputInfo());
        if (get<2>(temp)!=-1){
            UI->write(temp);
        }
    }
    tuple<string,string,float> inputInfo(tuple<string,int> temp)
    {
        for (Product* pro : productList) {
            Detail det = pro->getProductDetail();
            if (det.productName == get<0>(temp)) {
                pro->writeSatisfaction(get<1>(temp));
                return make_tuple(pro->getSellerID(),det.productName,pro->getProductSatisfaction());
            }
        }
        return make_tuple("","",-1.0);
    }

};

class ShowStaticsUI {
private:
public:
    void startInterface() {
        fprintf(out_fp, "5.1. 판매 상품 통계\n");
    }
    void write(vector<tuple<string,int,float>> temp){
        fprintf(out_fp, "> ");
        for(auto it=temp.begin();it!=temp.end();it++){
            fprintf(out_fp,"%s %d %d\n",get<0>(*it).c_str(),get<1>(*it),lround(get<2>(*it)));
        }
        fprintf(out_fp,"\n");
    }
};
class ShowStatics {
private:
    ShowStaticsUI* UI;
public:
    ShowStatics() {
        UI = new ShowStaticsUI();
        UI->startInterface();
        UI->write(currentUser->getSoldStat());
    }
};

void doTask(){
    int menu_level_1 = 0, menu_level_2=0, is_program_exit=0;
    while(!is_program_exit){
        fscanf(in_fp, "%d %d", &menu_level_1, &menu_level_2);
        switch ( menu_level_1) {
            case 1:
                switch (menu_level_2) {
                    case 1:{
                        Join* joi = new Join();
                        delete joi;
                        break;
                    }
                    case 2:{
                        Withdrawal* with = new Withdrawal();
                        delete with;
                        break;
                    }
                    default:
                        break;
                }
                break;
            case 2:
                switch (menu_level_2) {
                    case 1:{
                        Login* log = new Login();
                        delete log;
                        break;
                    }
                    case 2:{
                        Logout* log = new Logout();
                        delete log;
                        break;
                    }
                    default:
                        break;
                }
                break;
            case 3:
                switch (menu_level_2) {
                    case 1:{
                        AddSellingProduct* add = new AddSellingProduct();
                        delete add;
                        break;
                    }
                    case 2:{
                        ShowSellingProduct* show = new ShowSellingProduct();
                        delete show;
                        break;
                    }
                    case 3:{
                        ShowSoldOutProduct* show = new ShowSoldOutProduct();
                        delete show;
                        break;
                    }
                    default:
                        break;
                }
                break;
            case 4:
                switch (menu_level_2) {
                    case 1:{
                        SearchProduct* search = new SearchProduct();
                        delete search;
                        break;
                    }
                    case 2:{
                        Purchase* pur = new Purchase();
                        delete pur;
                        break;
                    }
                    case 3:{
                        ShowHistory* show = new ShowHistory();
                        delete show;
                        break;
                    }
                    case 4:{
                        WriteSatisfaction* write = new WriteSatisfaction();
                        delete write;
                        break;
                    }
                    default:
                        break;
                }
                break;
            case 5:{
                ShowStatics* show = new ShowStatics();
                delete show;
                break;
            }
            case 6:
                is_program_exit=1;
                fprintf(out_fp,"6.1 종료\n");
                break;
            default:
                break;
        }
    }
    fclose(in_fp);
    fclose(out_fp);
}
int main(){
    in_fp = fopen("input.txt", "r+");
    out_fp = fopen("output.txt", "w+");
    doTask();
    return 0;
}
