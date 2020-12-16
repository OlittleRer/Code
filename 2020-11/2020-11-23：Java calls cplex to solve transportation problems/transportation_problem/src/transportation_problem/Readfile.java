package transportation_problem;

import java.io.*;
import java.util.*;

/**
 * This class is to read data from txt file
 * @param path: the file path to be read
 * @return return a data object
 * @throws IOException
 */
public class Readfile {

	List<transportation_node> transportationNodeList = new ArrayList<transportation_node>();
	transportation_relation transportationRelation;
	
	public Readfile(String path1,String path2) throws IOException {
		
		readtransportation_node(path1);
		transportation_relation(path2);
	}
	
	public void readtransportation_node(String path) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader(path));
		String line = new String();
		
		//¶ÁÈ¡±äÁ¿
	    br.readLine();
	    line = br.readLine();
	    String[] tokens = line.split("\\s+");
		while(tokens.length > 0) {
			transportation_node Temp = new transportation_node(tokens[0],Integer.parseInt(tokens[1]),Integer.parseInt(tokens[2]),Integer.parseInt(tokens[3]));
			transportationNodeList.add(Temp);
		    line = br.readLine();		    
		    tokens = line.split("\\s+");
		}
		br.close();
		
	}
	
	public void transportation_relation(String path) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader(path));
		String line[] = new String[100];
		int row = 0;
		line[row] = br.readLine();
		while(line[row] != null) {
			row++;
			line[row] = br.readLine();
		}
		
		String[] tokens = line[0].split("\\s+");
		int column = tokens.length;
		int [] dis = new int[(row-1)*column];
		
		for (int i = 1; i < row; i++) {
			tokens = line[i].split("\\s+");
			for (int j = 1; j <= column; j++) {
				dis[(column)*(i-1)+j-1] = Integer.parseInt(tokens[j]);
			}
		}
		transportationRelation = new transportation_relation(dis);
		br.close();
	}
}
