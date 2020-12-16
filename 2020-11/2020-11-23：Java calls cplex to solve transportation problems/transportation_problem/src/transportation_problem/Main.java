package transportation_problem;

import java.io.IOException;
import java.util.List;
import ilog.concert.IloException;

public class Main {
	public static void main(String[] args) throws IOException, IloException {
		Readfile file = new Readfile("transportation_node.txt","transportation_relation.txt");
		List<transportation_node> transportationNodeList = file.transportationNodeList;
		transportation_relation transportationRelation = file.transportationRelation;
		
		model_transportation model = new model_transportation();
		model.bulidModel(transportationNodeList, transportationRelation);
	}
}
