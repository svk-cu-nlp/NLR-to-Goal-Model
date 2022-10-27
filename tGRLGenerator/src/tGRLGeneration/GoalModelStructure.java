package tGRLGeneration;
import java.util.*;
public class GoalModelStructure {
	String goal="", actor="", decompositionType="";
	ArrayList<String>subgoalList;
	ArrayList<String>softgoalList;
	public GoalModelStructure()
	{
		subgoalList = new ArrayList<String>();
	}
	public String getGoal() {
		return goal;
	}
	public void setGoal(String goal) {
		this.goal = goal;
	}
	public String getActor() {
		return actor;
	}
	public void setActor(String actor) {
		this.actor = actor;
	}
	public String getDecompositionType() {
		return decompositionType;
	}
	public void setDecompositionType(String decompositionType) {
		this.decompositionType = decompositionType;
	}
	public ArrayList<String> getSubgoalList() {
		return subgoalList;
	}
	public void setSubgoalList(ArrayList<String> subgoalList) {
		this.subgoalList = subgoalList;
	}
	
	
}
