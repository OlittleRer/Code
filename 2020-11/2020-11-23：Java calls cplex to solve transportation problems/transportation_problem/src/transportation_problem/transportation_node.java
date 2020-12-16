package transportation_problem;

/**
 * This class is to define the transportation_node
 * @param Property of node
 * @return a node object
 */

public class transportation_node {
	String NodeName;
	int quantity;
	int isSource;		
	int id;
	public transportation_node(String NodeName,int quantity,int isSource,int id) {
		this.NodeName = NodeName;
		this.quantity = quantity;
		this.isSource = isSource;
		this.id = id;
	} 

	public boolean isSource() {
		if(this.isSource == 1) {
			return true;
		}
	return false;
	}
}
