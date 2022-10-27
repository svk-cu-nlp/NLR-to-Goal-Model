package tGRLGeneration;
import java.util.*;
public class MetaData {
	ArrayList<String>goalList;
	ArrayList<String>subgoalList;
	String decompositionType="";
	public MetaData()
	{
		goalList=new ArrayList<String>();
		subgoalList=new ArrayList<String>();
	}
	public ArrayList<String> getGoalList() {
		return goalList;
	}
	public void setGoalList(ArrayList<String> goalList) {
		this.goalList = goalList;
	}
	public ArrayList<String> getSubgoalList() {
		return subgoalList;
	}
	public void setSubgoalList(ArrayList<String> subgoalList) {
		this.subgoalList = subgoalList;
	}
	public String getDecompositionType() {
		return decompositionType;
	}
	public void setDecompositionType(String decompositionType) {
		this.decompositionType = decompositionType;
	}
	
}
