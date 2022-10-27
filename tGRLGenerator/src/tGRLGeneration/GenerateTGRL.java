package tGRLGeneration;
import java.io.*;
import java.util.*;
class Generation{
	ArrayList<GoalModelStructure>gmsList;
	HashMap<String, ArrayList<GoalModelStructure>>gmsMap;
	String doc ="tgrl {";
	// Creates a FileOutputStream
	FileOutputStream file = null;

	// Creates a PrintStream
	PrintStream output = null;
	public Generation()
	{
		try {
			file = new FileOutputStream("tgrl.txt");
			output = new PrintStream(file);
		} catch (Exception e) {
			// TODO: handle exception
		}
		gmsList=new ArrayList<GoalModelStructure>();
		gmsMap=new HashMap<>();
		
	}
	public void tGRLCreator(String actor, String goal, String decompositionType, ArrayList<String>subgoalList)
	{
		for(GoalModelStructure gms: gmsList)
		{
			String actor1 = gms.getActor();
			String goal1 = gms.getGoal();
			String decomString = gms.getDecompositionType();
			ArrayList<String>subgoalList1 = gms.getSubgoalList();
		}
		String doc = "goal "+goal+" { \n decompositionType: "+decompositionType+"\n subgoal: ";
		for(String s:subgoalList) {
			doc = doc + s+", ";
			
		}
		doc = doc.trim();
		doc = doc.substring(0, doc.length() - 1);
		doc = doc+"\n }";
		System.out.println(doc);
	}
	public void tGRLCreator2()
	{
		ArrayList<String>subgoalList = new ArrayList<String>();
		
		int count = 1;
		String actor = "";
		ArrayList<String>subgoalList1= new ArrayList<>();
		GoalModelStructure gms1 = gmsList.get(0);
		actor = gms1.getActor();
		doc = doc+" \n actor "+actor+"{";
		//System.out.println("Actor is : "+gms1.getActor());
		for(GoalModelStructure gms: gmsList)
		{
			String actor1 = gms.getActor();
			if(count == 1)
			{
				actor = actor1;
			}
			count++;
			String goal = gms.getGoal();
			String decompositionType = gms.getDecompositionType();
			//System.out.println(actor+" "+ goal+" "+decompositionType);
			subgoalList1 = gms.getSubgoalList();
			doc = doc+ "\n   goal "+goal+" { \n     decompositionType: "+decompositionType+"\n     subgoal: ";
			//System.out.println("Subgoals..........");
			for(String s: subgoalList1)
			{
				//System.out.println(s);
				doc = doc + s+", ";
				subgoalList.add(s);
			}
			
			doc = doc.trim();
			doc = doc.substring(0, doc.length() - 1);
			doc = doc+"\n  }";
		}
		for(String s:subgoalList)
		{
			doc = doc + "\n goal "+s;
		}
		doc = doc + "\n }\n}";
		System.out.println(doc);
		output.println(doc);
		output.close();
	}
	public void parser(String line)
	{
		String actor = "";
		String goal = "";
		ArrayList<String>subgoalList = new ArrayList<String>();
		
		String decompositionType = "";
		try {
			StringTokenizer st = new StringTokenizer(line,";");
			while(st.hasMoreTokens())
			{
				String token = st.nextToken();
				
				//System.out.println(token);
				if(token.contains("Actor:"))
				{
					StringTokenizer st2 = new StringTokenizer(token);
					actor = st2.nextToken();
					actor = "";
					while(st2.hasMoreTokens())
					{
						actor = actor+" "+st2.nextToken();
					}
					actor = actor.trim();
					//System.out.println(actor);
				}
				if(token.contains("Goal:"))
				{
					StringTokenizer st2 = new StringTokenizer(token);
					goal = st2.nextToken();
					goal = "";
					while(st2.hasMoreTokens())
					{
						goal = goal+" "+st2.nextToken();
					}
					goal = goal.trim();
					//System.out.println(goal);
				}
				if(token.contains("DecompositionType:"))
				{
					StringTokenizer st2 = new StringTokenizer(token);
					decompositionType = st2.nextToken();
					decompositionType = st2.nextToken();
					//System.out.println(decompositionType);
				}
				if(token.contains("Subgoal:"))
				{
					StringTokenizer st2 = new StringTokenizer(token,",");
					while(st2.hasMoreTokens())
					{
						String sg = st2.nextToken();
						if(sg.contains("Subgoal:"))
							sg = sg.substring(9);
						
						sg = sg.trim();
						subgoalList.add(sg);
					}
				}
				
			}
			System.out.println("Actor- "+actor+" Goal- "+goal+" DecomType-- "+decompositionType);
			System.out.println("subgoals...");
			for(String s:subgoalList)
			{
				System.out.println(s);
			}
			GoalModelStructure gms = new GoalModelStructure();
			gms.setActor(actor);
			gms.setGoal(goal);
			gms.setDecompositionType(decompositionType);
			gms.setSubgoalList(subgoalList);
			gmsList.add(gms);
			if(!gmsMap.containsKey(actor))
			{
				ArrayList<GoalModelStructure>glist=new ArrayList<GoalModelStructure>();
				glist.add(gms);
				gmsMap.put(actor, glist);
			}
			else
			{
				ArrayList<GoalModelStructure>glist=new ArrayList<GoalModelStructure>();
				glist = gmsMap.get(actor);
				glist.add(gms);
				gmsMap.put(actor, glist);
			}
			//tGRLCreator(actor, goal, decompositionType, subgoalList);
		} catch (Exception e) {
			// TODO: handle exception
		}
	}
	public void controller(String file)
	{
		String line="";
		BufferedReader br = null;
		try {
			br = new BufferedReader(new FileReader(file));
			line = br.readLine();
			while(line!=null)
			{
				System.out.println(line+" \n --------------------------------------");
				parser(line);
				line = br.readLine();
			}
			
			 for(Map.Entry m : gmsMap.entrySet())
			 {    
				 ArrayList<GoalModelStructure>glist=new ArrayList<GoalModelStructure>();
				 glist=(ArrayList<GoalModelStructure>) m.getValue();
				 System.out.println("===============================Actor: "+m.getKey()+"\n======================================");
				 for(GoalModelStructure gm : glist)
				 {
					 System.out.println("Goal: "+gm.getGoal());
					 ArrayList<String>sl=gm.getSubgoalList();
					 System.out.println("Subgoals:=========================");
					 for(String s:sl)
					 {
						 System.out.println(s);
					 }
				 }
			 }  
		}
		catch(Exception e)
		{
			System.out.println(e.toString());
		}
		
	}
	
}
public class GenerateTGRL {

	public static void main(String[] args) {
		Generation gen = new Generation();
		gen.controller("majhong.txt");
		System.out.println("Generating TGRL.....");
		gen.tGRLCreator2();

	}

}
