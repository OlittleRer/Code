package simplex_method;

/**
 * @Author Simon
 * @Description 该类用于定义矩阵运算的方法,包括求行列式的值、求余子式、求矩阵的逆、求矩阵的转置、求数组的序、求矩阵的乘法等
 * @ClassName MatrixOperation
 * @Date 2020/9/24 11:09
 * @Version 1.0
 */
public class MatrixOperation {
    public static double [][] matrix_Inverse (double[][] origin) throws Exception {
        /**
         * @Author Simon
         * @Description 该方法用于求矩阵的逆
         * @Date 2020/9/26 14:42
         * @Param [origin]
         * @Retrun double[][]
         */
        // 验证矩阵的行列式是否等于零
        if(MatrixOperation.matrix_Det(origin) == 0){
            throw new Exception("矩阵不可逆");  //若输入的矩阵不可逆，则抛出异常
        }

        // 求矩阵的逆
        double[][] fin = new double[origin.length][origin[0].length];
        // 求二阶矩阵的逆
        if(origin.length == 2){
            fin[0][0] = origin[1][1];
            fin[0][1] = -origin[1][0];
            fin[1][1] = origin[0][0];
            fin[1][0] = -origin[0][1];
            fin = MatrixOperation.matrix_Transposed(fin);
            for(int i = 0; i < fin.length; i++){
                for(int j = 0; j < fin.length; j++){
                    fin[i][j] = fin[i][j]/(origin[0][0]*origin[1][1]-origin[0][1]*origin[1][0]);
                }
            }
            return fin;
        }
        // 求其他阶矩阵的逆
        int[] ser = new int[2];
        for(int i = 0; i < fin.length; i++){
            for(int j = 0; j < fin[0].length; j++){
                ser[0] = i;
                ser[1] = j;
                try {
                    fin[i][j] = pow(-1, i + j) * MatrixOperation.matrix_Det(MatrixOperation.matrix_Minor(origin, ser)) / MatrixOperation.matrix_Det(origin);
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        }
        fin = matrix_Transposed(fin);
        return fin;
    }
    public static double[][] matrix_Minor(double[][] origin,int[] ser) throws Exception {
        /**
         * @Author Simon
         * @Description 该方法用于返回矩阵的余子式(二维矩阵以上)
         * @Date 2020/9/24 12:59
         * @Param [origin, ser]
         * @Retrun double[][]
         */
        if(origin.length < 3){
            throw new Exception("请输入二阶以上矩阵");
        }
        double[][] fin = new double[origin.length-1][origin[0].length-1];
        for(int i = 0; i < fin.length; i++){
            for(int j = 0; j < fin[0].length; j++){
                if(i < ser[0]){
                    if(j < ser[1]){
                        fin[i][j] = origin[i][j];
                    }
                    else{
                        fin[i][j] = origin[i][j+1];
                    }
                }
                else{
                    if(j < ser[1]){
                        fin[i][j] = origin[i+1][j];
                    }
                    else{
                        fin[i][j] = origin[i+1][j+1];
                    }
                }

            }
        }
        return fin;
    }
    public static double matrix_Det(double[][] origin) {
        /**
         * @Author Simon
         * @Description 该方法用于求解并返回行列式[origin]的值
         * @Date 2020/9/23 21:00
         * @Param [origin]
         * @Retrun double[]
         */
        double fin = 0;  //定义return的变量，代表行列式的值

        int bin1 = -1;  //定义改变符号的变量1
        int bin2 = -1;  //定义改变符号的变量2

        int [] ser = new int[2];  //定义所选矩阵元素的行和列

        //  设置迭代初始值
        if(origin.length == 2){
            return origin[0][0]*origin[1][1] - origin[0][1]*origin[1][0];
        }

        //  迭代过程
        for(int i = 0; i < origin.length; i++){
            bin2 = bin2 * bin1;
            ser[0] = 0;
            ser[1] = i;
            try {
                fin = fin + origin[0][i] * bin2 * matrix_Det(matrix_Minor(origin,ser));
            }catch (Exception e){
                e.printStackTrace();
            }
        }

        return fin;
    }
    public static double [][] matrix_Transposed(double[][] origin){
        /**
         * @Author Simon
         * @Description 该方法用于返回矩阵[origin]的转置矩阵
         * @Date 2020/9/24 20:17
         * @Param [origin]
         * @Retrun double[][]
         */
        double [][] fin = new double[origin.length][origin[0].length];
        for(int i = 0; i < origin.length; i++){
            for(int j= 0; j< origin[0].length; j++){
                if(i == j){
                    fin[i][j] = origin[i][j];
                }
                else{
                    fin[i][j] = origin[j][i];
                }
            }
        }
        return fin;
    }
    public static double [][] matrix_Multiplication(double[][] origin1, double[][] origin2) throws Exception{
        /**
         * @Author Simon
         * @Description 该方法用于返回两个矩阵的乘积origin1*origin2
         * @Date 2020/9/25 8:05
         * @Param [origin1, origin2]
         * @Retrun double[][]
         */
        // 验证origin1矩阵的的列数是否和origin2矩阵的行数相等
        if(origin1[0].length != origin2.length){
            throw new Exception("两个矩阵无法相乘");  //若输入的两个矩阵无法相乘，则抛出异常
        }

        double[][] fin = new double[origin1.length][origin2[0].length];
        for(int i = 0; i < fin.length; i++){
            for(int j =0; j < fin[0].length; j++){
                try{
                    fin[i][j] = oneD_Matrix_Multiplication(get_Matrix_Row(origin1,i),get_Matrix_Col(origin2,j));
                }catch(Exception e){
                    e.printStackTrace();
                }
            }
        }
        return fin;
    }
    public static double[] matrix_Multiplication(double[][] origin1, double[] origin2) throws Exception{
        // 验证origin1矩阵的的列数是否和origin2向量的行数相等
        if(origin1[0].length != origin2.length){
            throw new Exception("两个矩阵无法相乘");  //若输入的两个矩阵无法相乘，则抛出异常
        }

        double[] fin = new double[origin1.length];
        for(int i = 0; i < fin.length; i++){
            try{
                fin[i] = oneD_Matrix_Multiplication(get_Matrix_Row(origin1,i),origin2);
            }catch(Exception e){
                e.printStackTrace();
            }
        }
        return fin;
    }
    public static double[] matrix_Multiplication(double[] origin1, double[][] origin2) throws Exception{
        // 验证origin1矩阵的的列数是否和origin2向量的行数相等
        if(origin1.length != origin2.length){
            throw new Exception("两个矩阵无法相乘");  //若输入的两个矩阵无法相乘，则抛出异常
        }

        double[] fin = new double[origin1.length];
        for(int i = 0; i < fin.length; i++){
            try{
                fin[i] = oneD_Matrix_Multiplication(origin1,get_Matrix_Col(origin2,i));
            }catch(Exception e){
                e.printStackTrace();
            }
        }
        return fin;
    }
    public static double[] get_Matrix_Row(double [][] origin, int r){
        /**
         * @Author Simon
         * @Description 该方法用于返回矩阵(二维)的某一行
         * @Date 2020/9/25 8:26
         * @Param [origin, r]
         * @Retrun double[]
         */
        double[] fin = new double[origin[0].length];
        for(int i = 0; i < fin.length; i++){
            fin[i] = origin[r][i];
        }
        return fin;
    }
    public static double[] get_Matrix_Col(double [][] origin, int r){
        /**
         * @Author Simon
         * @Description 该方法用于返回矩阵的某一列
         * @Date 2020/9/25 13:57
         * @Param [origin, r]
         * @Retrun double[]
         */
        double[] fin = new double[origin.length];
        for(int i = 0; i < fin.length;i++){
            fin[i] = origin[i][r];
        }
        return fin;
    }
    public static double oneD_Matrix_Multiplication(double[] originD1, double[] originD2) throws Exception{
        /**
         * @Author Simon
         * @Description 该方法用于返回两个向量的乘积
         * @Date 2020/9/25 8:15
         * @Param [originD1, originD2]
         * @Retrun double
         */
        // 验证originD1向量的长度是否和originD2相等
        if(originD1.length != originD2.length){
            throw new Exception("两个向量无法相乘");  //若输入的两个向量无法相乘，则抛出异常
        }
        double fin = 0;
        for(int i = 0; i < originD1.length; i++){
            fin = fin + originD1[i]*originD2[i];
        }
        return fin;
    }
    public static double pow(int x, int y){
        double p = 1;
        for(int i = 0; i < y; i++){
            p = p * x;
        }
        return p;
    }
    public static int get_Ser(int[] seq){
        /**
         * @Author Simon
         * @Description 用于行列式计算，求一个排列的序
         * @Date 2020/9/24 9:52
         * @Param [seq]
         * @Retrun int
         */
        int ser = 0;
        for(int i = 0; i < seq.length-1; i++){
            for(int j = i+1; j < seq.length; j++){
                if(seq[i] > seq[j]){
                    ser++;
                }
            }
        }
        return ser;
    }
}
