import javax.swing.JFrame;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JComboBox;
import javax.swing.JScrollPane;
import javax.swing.ScrollPaneConstants;
import javax.swing.JOptionPane;
import javax.swing.ImageIcon;
import java.awt.Font;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.util.ArrayList;          //used in the bill(); function
public class MyFrame implements ActionListener
{
	JComboBox[] box;                        //declaring an array of combo box
	JLabel menu;			                //contains the names and combo boxes of items
	JScrollPane scrollPane;	                //contains the menu label
	JLabel[] name,price;                    //labels to display name and price on the JFrame
	JFrame frame = new JFrame("Menu");
	JButton button;
	int items = 36;                         //stores the number of items
	String[] item;                          //array to store the names of the items
	int[] price1;                           //array to store the price of items
	int[] qty;                              //array to store the quantity of the items
	int[] sum = new int[items];             //storing price*qty for each item
	JLabel[] SrNo;
	int total=0;                            //final amount
	
	
	/*
	  To add a new item:
	  1)line 24 : change the number of items
	  2)add the item to the item[] array  
	  3)add the price to the price1[] array
	*/
	
	
	MyFrame()
	{
		qty = new int[items];
		for(int i = 0; i<items; i++)
		{
			qty[i] = 0;
		}
		
		for(int i = 0; i<items; i++)
		{
			sum[i] = 0;
		}
			
		
		box = new JComboBox[items];   //initializing the array
		Integer[] numbers = {0,1,2,3,4,5,6,7,8,9};
		for(int i = 0; i<items; i++)
		{
			box[i] = new JComboBox(numbers);  //assigning the array
			box[i].addActionListener(this);
		}
		
		
		//label for SrNo
		SrNo = new JLabel[items];
		for(int i = 0; i<items; i++)
		{
			SrNo[i] = new JLabel((i+1)+")");   
			//i+1 is integer but parameter is String
			//as we have added  +")" so it accepts integer variables to be added
			//but if it were alone then we have to use Integer.toString(i+1); to pass it as a string
		}		
		
		//initializing the items
		item = new String[items];
		item[0] = "Spl. Kadai Tarkari";
		item[1] = "Spl. Sabji Bahar";
		item[2] = "Paneer Tikka Masala";
		item[3] = "Alu Matar";
		item[4] = "Veg. Kurma";
		item[5] = "Bhendi Masala";
		item[6] = "Baigan Masala";
		item[7] = "Veg.Chana Masala";
		item[8] = "Alu Palak";
		item[9] = "Dal Fry";
		item[10] = "Dal Fry Tadka";
		item[11] = "Dal Palak";
		item[12] = "Alu Gobi";
		item[13] = "Alu Methi";
		item[14] = "Methi Masala";
		item[15] = "Green Peas Masala";
		item[16] = "Mix Vegetable";
		item[17] = "Veg. Kolhapuri";
		item[18] = "Mushroom Masala";
		item[19] = "Malai Mutter Methi";
		item[20] = "Kashmiri Veg.";
		item[21] = "Veg. Moghlai";
		item[22] = "Kaju Curry";
		item[23] = "Paneer Pasand";
		item[24] = "Paneer Lazeez";
		item[25] = "Paneer Kadai";
		item[26] = "Paneer Handi";
		item[27] = "Paneer Hariyali";
		item[28] = "Paneer Kolhapuri";
		item[29] = "Shahi Paneer";
		item[30] = "Paneer Masala";
		item[31] = "Paneer Baby Corn Masala";
		item[32] = "Paneer Kofta";
		item[33] = "Veg. Tiranga";
		item[34] = "Hara Bara Kabab Masala";
		item[35] = "Extra Roti";
		
		name = new JLabel[items];
		for(int i = 0; i<items; i++)
		{
			name[i] = new JLabel(item[i]);     //assigning the array
		}
		
		
		//initializing the prices
		price1 = new int[items];
		price1[0] = 180;
		price1[1] = 180;
		price1[2] = 200;
		price1[3] = 130;
		price1[4] = 130;
		price1[5] = 130;
		price1[6] = 130;
		price1[7] = 130;
		price1[8] = 130;
		price1[9] = 105;
		price1[10] = 115;
		price1[11] = 130;
		price1[12] = 140;
		price1[13] = 140;
		price1[14] = 140;
		price1[15] = 140;
		price1[16] = 150;
		price1[17] = 150;
		price1[18] = 190;
		price1[18] = 180;
		price1[19] = 180;
		price1[20] = 190;
		price1[21] = 200;
		price1[22] = 200;
		price1[23] = 200;
		price1[24] = 200;
		price1[25] = 200;
		price1[26] = 200;
		price1[27] = 200;
		price1[28] = 200;
		price1[29] = 200;
		price1[30] = 170;
		price1[31] = 200;
		price1[32] = 200;
		price1[33] = 200;
		price1[34] = 200;
		price1[35] = 5;
		
		price = new JLabel[items];
		for(int i = 0; i<items; i++)
		{
			price[i] = new JLabel("Rs. "+price1[i]);     //assigning the array
		}
		
		//name[15].setBorder(BorderFactory.createLineBorder(Color.black));
		//name[31].setBorder(BorderFactory.createLineBorder(Color.black));
		//price[31].setBorder(BorderFactory.createLineBorder(Color.black));
		
		
		menu = new JLabel();
		menu.setLayout(null);
		menu.setBackground(new Color(255,235,90));
		menu.setOpaque(true);
		
		
		scrollPane = new JScrollPane(menu);
		scrollPane.setBounds(0,0,870,800);
		scrollPane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
		
	    double x = items;
	    //we create a double variable because as items is int data type so when item = 37, then item/2 = 18
	    //also Math.ceil(item/2) = 18   
		int itemsInFirstColumn = (int) Math.ceil(x/2); 
		//Math.ceil() returns double value so we type cast it to int
		//for ex. items = 36 then each column has 18 items
		//if items = 39 then 1st column has 19 items and 2nd column will have 18 items
		
		menu.setPreferredSize(new Dimension(850, 100+(itemsInFirstColumn*40)));
		
		//----------adding serial number---------------------
		for(int i = 0; i<itemsInFirstColumn; i++)                                     //adding column 1  of serial no. to the menu
		{
			menu.add(SrNo[i]);
			SrNo[i].setFont(new Font("Cascadia Code",Font.BOLD,16));
			SrNo[i].setBounds(45, 70+(i*40), 30, 24);
		} 
		for(int i = itemsInFirstColumn; i<items; i++)                                 //adding column 2 to the menu
		{
			menu.add(SrNo[i]);
			SrNo[i].setFont(new Font("Cascadia Code",Font.BOLD,16));
			SrNo[i].setBounds(495, 70+((i-itemsInFirstColumn)*40), 30, 24);
		}
		
        //---------adding name-----------
		for(int i = 0; i<itemsInFirstColumn; i++)                                     //adding column 1  of name to the menu
		{
			menu.add(name[i]);
			name[i].setFont(new Font("Cascadia Code",Font.BOLD,16));
			name[i].setBounds(80, 70+(i*40), 180, 24);
		}
		for(int i = itemsInFirstColumn; i<items; i++)                                 //adding column 2 to the menu
		{
			menu.add(name[i]);
			name[i].setFont(new Font("Cascadia Code",Font.BOLD,16));
			name[i].setBounds(530, 70+((i-itemsInFirstColumn)*40), 200, 24);
		}
		
		
		//------------adding prices------------------
		for(int i = 0; i<itemsInFirstColumn; i++)                                     //adding column 1  of prices to the menu
		{
			menu.add(price[i]);
			price[i].setFont(new Font("Cascadia Code",Font.BOLD,16));
			price[i].setBounds(265, 70+(i*40), 60, 24);
		}
		for(int i = itemsInFirstColumn; i<items; i++)                                 //adding column 2 to the menu
		{
			menu.add(price[i]);
			price[i].setFont(new Font("Cascadia Code",Font.BOLD,16));
			price[i].setBounds(735, 70+((i-itemsInFirstColumn)*40), 60, 24);
		}
		
		
		//------------adding combo box-------------------------
		for(int i = 0; i<itemsInFirstColumn; i++)                                     //adding column 1 of combo box to the menu
		{
			menu.add(box[i]);
			box[i].setBounds(330, 70+(i*40), 40, 24);
		}
		for(int i = itemsInFirstColumn; i<items; i++)                                 //adding column 2 to the menu
		{
			menu.add(box[i]);
			box[i].setBounds(800, 70+((i-itemsInFirstColumn)*40), 40, 24);
		}
		
		JLabel label1 = new JLabel("Punjabi");
		label1.setFont(new Font("Harrington",Font.PLAIN,100));
		label1.setForeground(Color.red);
		label1.setBounds(1020,200,500,100);
		//label1.setBackground(new Color(40,255,50));
		//label1.setOpaque(true);
		//label1.setBorder(BorderFactory.createDashedBorder(Color.black));
		
		JLabel label2 = new JLabel("Dhaba");
		label2.setFont(new Font("Harrington",Font.PLAIN,100));
		label2.setForeground(Color.red);
		label2.setBounds(1050,320,300,100);
		//label.setBackground(new Color(40,255,50));
		//label2.setOpaque(true);
		//label.setBorder(BorderFactory.createDashedBorder(Color.black));
		
		JLabel label3 = new JLabel("Menu");
		label3.setFont(new Font("Comic Sans",Font.PLAIN,35));
		label3.setBounds(390,0,100,50);
		label3.setForeground(new Color(51,153,255));
		
		button = new JButton("Submit");
		button.setFont(new Font("Poor Richard",Font.PLAIN,35));
		button.setBounds(1110,650,150,40);
		button.setBorder(BorderFactory.createEtchedBorder());
		button.setFocusable(false);
		button.addActionListener(this);
		
		ImageIcon icon1 = new ImageIcon("C:\\Users\\imrat\\Documents\\Java Files\\bhangra.jpg");
		JLabel label4 = new JLabel();
		label4.setIcon(icon1);
		label4.setBounds(870,140,200,300);

		ImageIcon icon2 = new ImageIcon("C:\\Users\\imrat\\Documents\\Java Files\\bhangra1.jpg");
		JLabel label5 = new JLabel();
		label5.setIcon(icon2);
		label5.setBounds(1370,140,200,300);
		
		menu.add(label3);
		frame.add(scrollPane);
		
		frame.add(label1);
		frame.add(label2);
		frame.add(label4);
		frame.add(label5);
		frame.add(button);
		
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(1800,815);
		frame.getContentPane().setBackground(new Color(255,255,120));
		frame.setLayout(null);
		frame.setLocationRelativeTo(null);
		frame.setVisible(true);
	}
	
	@Override
	public void actionPerformed(ActionEvent e)
	{		
		for(int i = 0; i<items; i++)
		{
			if(e.getSource()==box[i])
			{
				qty[i] = (int)box[i].getSelectedItem();
			}
		}
		
		int response=1;
		if(e.getSource()==button)
		{
			response = JOptionPane.showConfirmDialog(null,"Are you sure?","Confirmation",JOptionPane.YES_NO_OPTION);
			if(response == 0)
			{
				frame.dispose();
				bill();
			}
		}
		
		
	}
	
	public void bill()
	{
		int itemNo = 0;       //stores the number of items bought
		ArrayList<Integer> itemCode = new ArrayList<Integer>();   //for storing array index of items bought
		for(int i = 0; i<36; i++)
		{
			sum[i] = price1[i]*qty[i];
			if(sum[i]>0)
			{
				itemNo++;
				total = total + sum[i];
				itemCode.add(i);
			}
		}
		
		JLabel[] srNo = new JLabel[itemNo];
		JLabel[] Name = new JLabel[itemNo];
		JLabel[] QTY = new JLabel[itemNo];
		JLabel[] Price = new JLabel[itemNo];
		JLabel[] Amount = new JLabel[itemNo];
		
		
		
		for(int i = 0; i<itemNo; i++)
		{
			srNo[i] = new JLabel((i+1)+")");
			Name[i] = new JLabel(item[itemCode.get(i)]); 
			//adding the name of the item bought using the index of the bought items stored in the ArrayList
			//to get the stored items index in an ArrayList we use itemCode.get(i) where 'i' is the index of element
			//to be retrieved
			
			QTY[i] = new JLabel(Integer.toString(qty[itemCode.get(i)])); 
			//qty[itemCode.get(i)] is an integer
			//x = new JLabel(String);   JLabel takes String argument
			//to convert integer to String we use Integer.toString(int); 
			
			Price[i] = new JLabel(Integer.toString(price1[itemCode.get(i)]));
			Amount[i] = new JLabel(Integer.toString(sum[itemCode.get(i)]));
			
		}
		
		/*for(int i = 0; i<36; i++)
		{
			if(sum[i]>0)
			{
				Name[i] = new JLabel(item[i]);
				Price[i] = new JLabel("Rs. "+price1[i]);
				QTY[i] = new JLabel(Integer.toString(qty[i]));
				Amount[i] = new JLabel(Integer.toString(sum[i]));
			}
		}
		*/
		
		
		//---------------designing the frame------------------
		JFrame Bill = new JFrame("BILL");
		Bill.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		JPanel billPanel = new JPanel();
		billPanel.setBackground(Color.white);
		billPanel.setLayout(null);
		billPanel.setPreferredSize(new Dimension(480,680));
		
		JLabel line1 = new JLabel("Punjabi Dhaba");
		line1.setFont(new Font("Harrington",Font.PLAIN,40));
		line1.setForeground(Color.red);
		line1.setBounds(110,20,300,50);
		
		JLabel line2 = new JLabel("Bill");
		line2.setFont(new Font("Berlin Sans FB Demi",Font.PLAIN,25));
		line2.setBounds(225,80,50,30);
		
		JLabel line3 = new JLabel("----------------------------------");
		line3.setFont(new Font("Consolas",Font.PLAIN,25));
		line3.setForeground(Color.orange);
		line3.setBounds(5,120,500,10);
		
		JLabel line4 = new JLabel(" Sr. No.     Name       \t                                Qty.    \t    Cost \t       Amt.");
		line4.setFont(new Font("Cooper Black",Font.PLAIN,16));
		line4.setForeground(Color.blue);
		line4.setBounds(0,125,500,30);
		//line4.setBorder(BorderFactory.createLineBorder(Color.black));
		
		JLabel billLabel = new JLabel();
		billLabel.setLayout(null);
		billLabel.setBackground(Color.white);
		billLabel.setOpaque(true);
		billLabel.setBounds(0,155,485,(itemNo*40));
		
		JScrollPane billScrollPane = new JScrollPane(billPanel);
		billScrollPane.setBounds(0,0,485,700);
		billScrollPane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
		
		for(int i = 0; i<itemNo; i++)
		{
			srNo[i].setBounds(20,(i*40),40,40);
			srNo[i].setFont(new Font("MV Boli",Font.PLAIN,16));
			billLabel.add(srNo[i]);
			
			Name[i].setBounds(80,(i*40),200,40);
			Name[i].setFont(new Font("MV Boli",Font.PLAIN,16));
			billLabel.add(Name[i]);
			
			QTY[i].setBounds(290,(i*40),40,40);
			QTY[i].setFont(new Font("MV Boli",Font.PLAIN,16));
			billLabel.add(QTY[i]);
			
			Price[i].setBounds(350,(i*40),60,40);
			Price[i].setFont(new Font("MV Boli",Font.PLAIN,16));
			billLabel.add(Price[i]);
			
			Amount[i].setBounds(420,(i*40),60,40);
			Amount[i].setFont(new Font("MV Boli",Font.PLAIN,16));
			billLabel.add(Amount[i]);
		}
		
//		for(int i = 0; i<itemNo; i++)
//		{
//			Name[i].setBounds(80,(i*40),200,40);
//			Name[i].setFont(new Font("MV Boli",Font.PLAIN,16));
//			billLabel.add(Name[i]);
//			//Name[i].setBorder(BorderFactory.createLineBorder(Color.black));   //to check label dimension
//		}
//		
//		for(int i = 0; i<itemNo; i++)
//		{
//			QTY[i].setBounds(290,(i*40),40,40);
//			QTY[i].setFont(new Font("MV Boli",Font.PLAIN,16));
//			billLabel.add(QTY[i]);
//			//QTY[i].setBorder(BorderFactory.createLineBorder(Color.black));   //to check label dimension
//		}
//		
//		for(int i = 0; i<itemNo; i++)
//		{
//			Price[i].setBounds(350,(i*40),60,40);
//			Price[i].setFont(new Font("MV Boli",Font.PLAIN,16));
//			billLabel.add(Price[i]);
//			//Price[i].setBorder(BorderFactory.createLineBorder(Color.black));  //to check label dimension
//		}
//		
//		for(int i = 0; i<itemNo; i++)
//		{
//			Amount[i].setBounds(420,(i*40),60,40);
//			Amount[i].setFont(new Font("MV Boli",Font.PLAIN,16));
//			billLabel.add(Amount[i]);
//			//Amount[i].setBorder(BorderFactory.createLineBorder(Color.black));   //to check label dimension
//		}
		
		JLabel line5 = new JLabel("----------------------------------");
		line5.setFont(new Font("Consolas",Font.PLAIN,25));
		line5.setForeground(Color.orange);
		line5.setBounds(5,155+(itemNo*40),500,10);
		
		JLabel line6 = new JLabel("Total     :              Rs. "+total);
		line6.setFont(new Font("Poor Richard",Font.PLAIN,22));
		line6.setBounds(290,165+(itemNo*40),210,40);
		
		JLabel line7 = new JLabel("----------------------------------");
		line7.setFont(new Font("Consolas",Font.PLAIN,25));
		line7.setForeground(Color.orange);
		line7.setBounds(5,205+(itemNo*40),500,10);
		
		JLabel line8 = new JLabel("**  Thank You  **");
		line8.setFont(new Font("Consolas",Font.PLAIN,20));
		line8.setBounds(140,235+(itemNo*40),400,40);
		
		JLabel line9 = new JLabel("** Please Visit Again **");
		line9.setFont(new Font("Consolas",Font.PLAIN,20));
		line9.setBounds(100,275+(itemNo*40),400,40);
		
		JButton newOrderButton = new JButton("New Order");
		newOrderButton.setFocusable(false);
		newOrderButton.setFont(new Font(null,Font.PLAIN,25));
		newOrderButton.setBounds(160,380+(itemNo*40),180,30);
		newOrderButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e)
			{
				new MyFrame();
			}
		});
		
		
		billPanel.add(line1);
		billPanel.add(line2);
		billPanel.add(line3);
		billPanel.add(line4);
		billPanel.add(line5);
		billPanel.add(line6);
		billPanel.add(line7);
		billPanel.add(line8);
		billPanel.add(line9);
		billPanel.add(billLabel);
		billPanel.add(newOrderButton);
		
		Bill.add(billScrollPane);
		
		Bill.setSize(490,700);
		//Bill.setResizable(false);
		Bill.getContentPane().setBackground(Color.white);
		Bill.setLayout(null);
		Bill.setLocationRelativeTo(null);
		Bill.setVisible(true);
	}
	
}

