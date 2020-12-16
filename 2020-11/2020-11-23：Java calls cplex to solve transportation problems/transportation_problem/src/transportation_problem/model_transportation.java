package transportation_problem;

import java.util.List;
import ilog.concert.IloException;
import ilog.concert.IloNumExpr;
import ilog.concert.IloNumVar;
import ilog.cplex.IloCplex;

/**
 * This class is to conduct a model in cplex and solve
 * @param problem parameter
 * @return return solve result
 * @throws IloException
 */

public class model_transportation {
	IloCplex cplex ;
	double objectiveValue;
	IloNumVar x[];
	int numOfPlants = 0;
	int numOfdestination = 0;
	/**
	 * This method is to bulidModel
	 * @param transportation_problem's data
	 * @return transportation_problem's model
	 * @throws IloException
	 */
	public void bulidModel(List<transportation_node> transportationNodeList,transportation_relation transportationRelation)throws IloException {
		this.cplex = new IloCplex();
		for(transportation_node tsNode : transportationNodeList){
			if (tsNode.isSource()) {
				numOfPlants++;
			}else {
				numOfdestination++;
			}
		}
		CreatDecisionVariab();
		CreatObjFunc(transportationRelation);
		CreatConstraints(transportationNodeList);
		Solve(transportationNodeList);
	}
	/**
	 * This method is to create decision variables
	 * @throws IloException
	 */
	public void CreatDecisionVariab() throws IloException{
		x = new IloNumVar[numOfPlants*numOfdestination];
		for (int i = 0; i < numOfPlants; i++) {
			for (int j = 0; j < numOfdestination; j++) {
				x[i*numOfdestination+j] = cplex.numVar(0, Double.MAX_VALUE,"x"+(i+1)+(j+1));
			}
		}
	}
	/**
	 * This method is to create objective function
	 * @throws IloException
	 */
	public void CreatObjFunc(transportation_relation transportationRelation) throws IloException{
		cplex.addMinimize(cplex.scalProd(x,transportationRelation.distance));
	}
	/**
	 * This method is to add constraints
	 * @throws IloException
	 */
	public void CreatConstraints(List<transportation_node> transportationNodeList) throws IloException {
		for(transportation_node tsNode : transportationNodeList){
			IloNumExpr left = cplex.linearNumExpr();
			if (tsNode.isSource()) {
				for(int i = 0;i<numOfdestination;i++) {
					left = cplex.sum(left,cplex.prod(1,x[tsNode.id*numOfdestination+i]));
				}
				cplex.addEq(left,tsNode.quantity);
			}else {
				for(int i = 0;i<numOfPlants;i++) {
					left = cplex.sum(left,cplex.prod(1,x[tsNode.id+i*numOfdestination]));
				}
				cplex.addEq(left,tsNode.quantity);
			}
		}
	}
	/**
	 * This method is to solve model
	 * @return values of objective function and decision variables
	 * @throws IloException
	 */
	public void Solve(List<transportation_node> transportationNodeList) throws IloException{
		cplex.setOut(null);
		if (cplex.solve()) {
			cplex.exportModel("111.lp");
			objectiveValue = cplex.getObjValue();
			System.out.println("最小运费为：" + objectiveValue);
			for (int i = 0; i < numOfPlants; i++) {
				for (int j = 0; j < numOfdestination; j++) {
					System.out.print(transportationNodeList.get(i).NodeName+" to "+transportationNodeList.get(numOfPlants+j).NodeName+" : ");
					System.out.println(cplex.getValue(x[i*numOfdestination+j]));
				}
			}
		}
	}
}
