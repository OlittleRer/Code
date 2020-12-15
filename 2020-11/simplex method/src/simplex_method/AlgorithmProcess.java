package simplex_method;

import java.io.*;
import java.util.ArrayList;

/**
 * @Author Simon
 * @Description 该类用于单纯形法求解线性规划
 * @ClassName AlgorithmProcess
 * @Date 2020/9/24 20:59
 * @Version 1.0
 */
public class AlgorithmProcess {
    public static void main(String[] args) {

        int jud = 1;  //用于文件输入的辨别变量，1代表C，2代表A，3代表b
        int type_Solution = 0;  //为0时唯一最优解，为1时无穷多解，为2时无界解,为3时无解
        String doc = "data1.txt";  //数据文件名称，"data1"为标准唯一解算例，"data2"为存在退化解算例，"data3"为存在无穷多解算例，"data4"为存在无界解算例，"data5"为存在大于零和等于0约束的算例，"data6"为无解算例

        ArrayList<Double> c_ = new ArrayList<>(); //用于读取文件时存储c
        ArrayList<ArrayList<Double>> A_ = new ArrayList<>(); //用于读取文件时存储A
        ArrayList<Double> b_ = new ArrayList<>(); //用于读取文件时存储b
        ArrayList<Integer> symbol = new ArrayList<>(); //用于读取文件时存储约束的符号

        //读取文件
        try {
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(
                            new FileInputStream(doc)));
            String line = in.readLine();  //从文件中读入一行
            String[] strArr;  //将读入的一行字符串以一维数组存储
            while(line != null){
                strArr = line.split(",");
                // 当出现空行时，更改当前需要填充的数组，顺序依次为c、A、b
                if(line.length() == 0){
                    jud = jud + 1;
                    line = in.readLine();  //从文件中读入一行
                    continue;
                }
                // 填充目标函数系数矩阵c
                if(jud == 1){
                    for(int i = 0; i < strArr.length; i++){
                        c_.add(Double.valueOf(strArr[i].toString()));
                    }
                }
                // 填充约束的系数矩阵A
                if(jud == 2){
                    ArrayList<Double> qp = new ArrayList<>();
                    for(int i = 0; i < strArr.length; i++){
                        qp.add(Double.valueOf(strArr[i].toString()));
                    }
                    A_.add(qp);
                }
                // 填充符号矩阵
                if(jud == 3){
                    for(int i = 0; i < strArr.length; i++){
                        int a = Integer.valueOf(strArr[i].toString());
                        symbol.add(Integer.valueOf(strArr[i].toString()));
                    }
                }

                // 填充约束值的矩阵
                if(jud == 4){
                    for(int i = 0; i < strArr.length; i++){
                        b_.add(Double.valueOf(strArr[i].toString()));
                    }
                }
                line = in.readLine();  //从文件中读入一行
            }
            in.close();
        } catch (FileNotFoundException e) {
            // TODO 自动生成的 catch 块
            e.printStackTrace();
        } catch (IOException e) {
            // TODO 自动生成的 catch 块
            e.printStackTrace();
        }

        //计算所需添加变量的个数
        int l = 0;
        for (int i = 0; i < symbol.size(); i++) {
            if (symbol.get(i) == -1) { //小于等于的约束
                l = l + 1;
            } else if (symbol.get(i) == 0) { //等于的约束
                l = l + 2;
            } else if (symbol.get(i) == 1) { //大于等于的约束
                l = l + 2;
            }
        }

        //定义标准型中需要的矩阵A、b、c
        double[] c = new double[c_.size()+l];  //定义目标函数的系数矩阵c
        double[][] A = new double[A_.size()][A_.get(0).size()+l];  //定义约束的系数矩阵A
        double[] b = new double[b_.size()];  //定义约束值的矩阵b
        int per = 0; // 需要添加人工变量的约束个数
        double M = 1000000; // 大M法中的“M”

        //填充A，b，c
        for(int i = 0; i < c_.size(); i++){
            c[i] = c_.get(i);
        }
        for(int i = 0; i < b_.size(); i++){
            b[i] = b_.get(i);
        }
        for(int i = 0; i < A.length; i++){
            for(int j = 0; j < A_.get(0).size(); j++){
                A[i][j] = A_.get(i).get(j);
            }
        }
        int k = 0;
        int or = A_.get(0).size(); //原始变量的个数
        while(k < A.length){
            sy:switch (symbol.get(k)){
                case -1:
                    c[or] = 0;
                    A[k][or] = 1;
                    or = or + 1;
                    k = k + 1;
                    break sy;
                case 0:
                case 1:
                    c[or] = 0;
                    c[or+1] = -M;
                    A[k][or] = -1;
                    A[k][or+1] = 1;
                    or = or + 2;
                    k = k + 1;
                    per = per + 1;
                    break sy;
            }
        }

        //  计算所需的变量初始化
        int[] x_B_Num = new int[A.length];  //定义存储基变量标号的一维数组
        int[] x_N_Num = new int[A[0].length - A.length];  //定义存储非基变量的一维数组

        double[] x_B = new double[A.length];  //定义基变量值的一维数组
        double[] enter_Jud = new double[x_N_Num.length];  //定义存储进基变量的判断数
        double[] exit_Jud = new double[x_B_Num.length];  //定义存储出基变量的判断数

        double[] c_B = new double[x_B_Num.length];  //定义存储基变量的目标函数系数的向量
        double[] c_N = new double[x_N_Num.length];  //定义存储非基变量的目标函数系数的向量
        double[] Y = new double[c_B.length];  //定义c_B*B逆
        double[] F = new double[x_B_Num.length];  //定义B逆*P
        double[][] B = new double[A.length][A.length];  // 定义存储基变量在约束表达式系数的矩阵

        int u = 0;  //定义循环次数
        int en = 0;  //定义当前的进基序号
        int ex = 0;  //定义当前的出基序号
        int[] ee = new int[2];  //定义当前的出基序号和判断是否退化

        //填充初始基变量和非基变量序号
        for(int i = 0; i < x_B_Num.length; i++){
            getJ:for(int j = A[0].length-1; j >=0; j--){
                if(A[i][j] != 0){
                    x_B_Num[i] = j + 1;
                    break getJ;
                }
            }
        }
        int judN = -1;
        int kN = 0;
        for(int i = 1; i < c.length+1; i++){
            getN:for(int j = 0; j < x_B_Num.length; j++){
                if(i == x_B_Num[j]){
                     judN = 1;
                     break getN;
                }
            }
            if(judN == -1){
                x_N_Num[kN] = i;
                kN = kN + 1;
            }
            judN = -1;
        }

        //求解
        do {
            // 更新相关变量
            for(int i = 0; i < B.length; i++){
                for(int j = 0; j < B[0].length; j++){
                    double oo = A[i][x_B_Num[j]-1];
                    B[i][j] = A[i][x_B_Num[j]-1];
                }
            }
            for(int i = 0; i < c_B.length; i++){
                c_B[i] = c[x_B_Num[i]-1];
            }
            for(int i = 0; i < c_N.length; i++){
                c_N[i] = c[x_N_Num[i]-1];
            }

            //确定进基变量序号
            try {
                x_B = MatrixOperation.matrix_Multiplication(MatrixOperation.matrix_Inverse(B), b);
                Y = MatrixOperation.matrix_Multiplication(c_B, MatrixOperation.matrix_Inverse(B));
            } catch (Exception e) {
                e.printStackTrace();
            }
            for (int i = 0; i < enter_Jud.length; i++) {
                try {
                    enter_Jud[i] = MatrixOperation.oneD_Matrix_Multiplication(Y, MatrixOperation.get_Matrix_Col(A, x_N_Num[i] - 1)) - c_N[i];
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            //判断是否有无穷多解
            if (jud_If_Inf(enter_Jud)){
                System.out.println("无穷多最优解");
                type_Solution = 1;
                break;
            }

            //判断是否无解
            int noS = 0;
            for(int i = 0; i < enter_Jud.length; i++){
                if(enter_Jud[i] >= 0){
                    noS = noS + 1;
                }
            }
            if(noS == enter_Jud.length){ //如果检验数全部大于等于0
                for(int i = 0; i < x_B_Num.length; i++){ //检验基变量是否还有非0的人工变量
                    for(int j = 0; j < per; j++){
                        if(x_B_Num[i] == c.length-j*2){
                            System.out.println("无解");
                            type_Solution = 3;
                            break;
                        }
                    }
                }

            }

            en = get_Minus_Min(enter_Jud); //得到进基变量在x_N_Num中的序号。如果返回-1则达到最优解
            //判断是否达到循环停止条件
            if (en == -1) {
                break;
            }

            //确定出基变量序号
            try {
                double[] ii = MatrixOperation.get_Matrix_Col(A, x_N_Num[en] - 1);
                F = MatrixOperation.matrix_Multiplication(MatrixOperation.matrix_Inverse(B), MatrixOperation.get_Matrix_Col(A, x_N_Num[en] - 1));
            } catch (Exception e) {
                e.printStackTrace();
            }
            for (int i = 0; i < exit_Jud.length; i++) {
                if (F[i] == 0) {
                    exit_Jud[i] = -1;
                } else {
                    if(F[i] == 0){
                        exit_Jud[i] = 1000;
                    }
                    else {
                        if(x_B[i] == 0 && F[i] < 0){  //处理特殊情况，当出现此情况时，i不可作为出基变量
                            exit_Jud[i] = 1000;
                        }
                        else {
                            exit_Jud[i] = x_B[i] / F[i];
                        }
                    }
                }
            }

            //判断是否有无界解
            if(jud_If_Endless(enter_Jud,exit_Jud)){
                System.out.println("无界解");
                type_Solution = 2;
                break;
            }

            ee = get_Positive_Min(exit_Jud); //ee[0]出基变量在x_B_Num中的序号。ee[1]若不等于0，则出现退化现象
            ex = ee[0];

            //判断是否出现退化现象
            if(ee[1] == 0){    //如果没有退化现象
            }
            else{    //如果出现退化现象 重新确定进基和出基变量
                en = get_Re_Minus_Min(enter_Jud, x_N_Num);
                ex = get_Re_Positive_Min(exit_Jud, x_B_Num);
            }

            //输出每次循环的结果
            u = u + 1;
            System.out.printf("第%d次迭代结果：",u);
            System.out.println("");
            System.out.println("[基变量]");
            for(int i = 0; i < x_B.length; i++){
                System.out.print(x_B_Num[i]+" ");
                System.out.println(x_B[i]);
            }
            System.out.print("[目标函数] ");
            try{
                System.out.println(MatrixOperation.oneD_Matrix_Multiplication(c_B,x_B));
            }catch (Exception e){
                e.printStackTrace();
            }

            //进基和出基操作
            int exchange = 0;
            exchange = x_B_Num[ex];
            x_B_Num[ex] = x_N_Num[en];
            x_N_Num[en] = exchange;
        }while(get_Minus_Min(enter_Jud) != -1);

        if(type_Solution == 0){ //若为唯一最优解，则输出最优解和目标函数
            //输出最终结果
            u = u + 1;
            System.out.printf("第%d次迭代结果(最终结果)：",u);
            System.out.println("");
            System.out.println("[基变量]");
            for(int i = 0; i < x_B.length; i++){
                System.out.print(x_B_Num[i]+" ");
                System.out.println(x_B[i]);
            }
            System.out.print("[目标函数] ");
            try{
                System.out.println(MatrixOperation.oneD_Matrix_Multiplication(c_B,x_B));
            }catch (Exception e){
                e.printStackTrace();
            }
        }
        else if(type_Solution == 1){ //若为无穷最优解，则只输出目标函数
            System.out.print("[目标函数] ");
            try{
                System.out.println(MatrixOperation.oneD_Matrix_Multiplication(c_B,x_B));
            }catch (Exception e){
                e.printStackTrace();
            }
        }
    }
    public static int get_Minus_Min(double[] origin){
        /**
         * @Author Simon
         * @Description 该方法用于得到enter_Jud里小于零的最小值，若均大于o，则返回-1
         * @Date 2020/9/25 16:16
         * @Param [origin]
         * @Retrun int
         */
        int s = -1;
        double a = 0;
        for(int i = 0; i < origin.length; i++){
            if((origin[i]) < 0 && (origin[i] < a)){
                a = origin[i];
                s = i;
            }
        }
        return s;
    }
    public static int[] get_Positive_Min(double[] origin){
        /**
         * @Author Simon
         * @Description 该方法用于得到exit_Jud里不小于零的最小值，若均小于o，则返回-1
         * @Date 2020/9/26 11:57
         * @Param [origin]
         * @Retrun int
         */
        int[] g = new int[2]; //int[0]是最小值下标 int[1]为0的时候无退化，为1的时候退化
        int s = -1;
        double a = 1000000;
        for(int i = 0; i < origin.length; i++){
            if((origin[i]) >= 0 && (origin[i] < a)){
                a = origin[i];
                s = i;
            }
        }
        g[0] = s;
        g[1] = 0;
        double o = origin[s];
        //判断是否有退化现象

        for(int i = 0; i < origin.length; i++){
            if(i==s){
                continue;
            }
            if(origin[i] == a){
                g[1] = 1;
            }
        }
        origin[s] = o;
        return g;
    }
    public static int get_Re_Positive_Min(double[] origin,int[] index){
        /**
         * @Author Simon
         * @Description 该方法用于得到exit_Jud里大于零的最小值，存在多个最小值时选取所对应变量下标最小的那一个（勃朗宁规则）
         * @Date 2020/9/27 10:30
         * @Param [origin]
         * @Retrun int
         */
        int s = -1;
        double a = 1000000;
        for(int i = 0; i < origin.length; i++){
            if((origin[i]) > 0 && (origin[i] < a)){
                a = origin[i];
                s = i;
            }
            if(origin[i] == a){   //如果当前值和当前最小值相同
                if (index[i] < index[s]){   //如果当前值所对应index中的值小于之前最有值序号所对应index中的值,则更新最小值情况
                    a = origin[i];
                    s = i;
                }
            }
        }
        return s;
    }
    public static int get_Re_Minus_Min(double[] origin,int[] index){
        /**
         * @Author Simon
         * @Description 该方法用于得到entry_Jud里小于零的最小值，选取所对应变量下标最小的那一个（勃朗宁规则）
         * @Date 2020/9/27 10:37
         * @Param [origin, index]
         * @Retrun int
         */
        int s = 0;
        double a = 1000;
        for(int i = 0; i < origin.length; i++){
            if((index[i] < index[s])){   //寻找index中最小值所对应的下标s
                a = origin[i];
                s = i;
            }
        }
        return s;
    }
    public static boolean jud_If_Inf(double[] enter){
        /**
         * @Author Simon
         * @Description 该方法用于判断是否有无穷多解（所有检验数大于等于0并且其中一个非基变量的检验数为0）
         * @Date 2020/9/27 15:23
         * @Param [origin]
         * @Retrun boolean
         */
        boolean b = false;
        int count = 0;
        int ifo = -1;
        for(int i = 0; i < enter.length; i++){
            if(enter[i] >= 0){
                count = count = count + 1;
            }
            if(enter[i] == 0){
                ifo = 0;
            }
        }
        if(count == enter.length && ifo == 0){
            b =true;
        }
        return  b;
    }
    public static boolean jud_If_Endless(double[] enter, double[] exit){
        /**
         * @Author Simon
         * @Description 该方法用于判断是否有无尽解（存在检验数小于等于0并且其所对应的出基变量判断值均小于0）
         * @Date 2020/9/27 15:30
         * @Param [origin, origin]
         * @Retrun boolean
         */
        boolean b = false;
        int info = -1;
        int info2 = 1;
        for(int i = 0; i < enter.length; i++){
            if(enter[i] <= 0){
                info = 1;
            }
        }
        for(int i = 0; i < exit.length; i++){
            if(exit[i] > 0){
                info2 = -1;
            }
        }
        if(info == 1 && info2 == 1){
            b = true;
        }
        return b;
    }
}
