library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

Entity Camera is 
Port (
      Y,UV: In std_logic_vector(7 downto 0);
  	  VSYNC,HREF,PCLK,FODD: In std_logic;
	  VSYNC_O,HREF_O,PCLK_O: Out std_logic;
---------------------------------------------------------------------------------
 	  SW  	   : IN  std_logic_vector(3 downto 0);
	  CLOCK_50 : IN  std_logic;      
      VGA_B    : OUT std_logic_vector(3 downto 0); 
      VGA_R    : OUT std_logic_vector(3 downto 0); 
      VGA_G    : OUT std_logic_vector(3 downto 0); 
      VGA_HS   : OUT std_logic; 
      VGA_VS   : OUT std_logic;
	-----------------------------
   -------------------------------------------
	  SRAM_ADDR :  out  std_logic_vector (17 downto 0 );
	  SRAM_DQ   : inout std_logic_vector (15 downto 0 );
   -------------------------------------------
	  SRAM_CE_N,SRAM_OE_N,SRAM_WE_N,SRAM_UB_N,SRAM_LB_N : inout std_logic
	-----------------------------
---------------------------------------------------------------------------------
	 );
End Camera;

Architecture behaviour of Camera is 

signal Count,first_data: std_logic:= '0'; 
signal Data1, Data2 : std_logic_vector (15 downto 0);
signal RESET :  std_logic;
-------------------------------------------------
signal VGA_MEM_BUSY : STD_LOGIC := '0' ;
signal CMR_MEM_BUSY : STD_LOGIC := '0' ;
signal VGA_RAM_ADDR : std_logic_vector (17 downto 0);
signal VGA_RAM_DATA : std_logic_vector (15 downto 0 );
signal CMR_RAM_ADDR : std_logic_vector (17 downto 0);
signal CMR_RAM_DATA : std_logic_vector (15 downto 0 );
signal CMR_WE 		: std_logic;
signal VGA_WE 		: std_logic;
------------------------------------------------------
------------------------------------------------------
signal Address:  std_logic_vector(17 downto 0);
signal Data	  :  std_logic_vector(15 downto 0);

SIGNAL  cl_count : integer := 0;      -- the number of lines has drawn
Signal  chcount  : INTEGER := 0;      -- line pixel counter
------------------------------------------------------
------------------------------------------------------
SIGNAL CLOCK_25 : std_logic;    --25Mhz clock
 
CONSTANT HFP : integer := 16;    --Front porch (horizontal) 0.6mus
CONSTANT HBP : integer := 48;    --Back porch (horizontal)  1.9mus
CONSTANT HSYNC_TIME  : integer := 96;  -- H_Sync pulse lenght 3.8mus
CONSTANT LINE_PIXELS : integer := 634; -- Display pixels in one line is 25.4 mus
			   -- total pixel in one line is 794, last 31.7 muSec

			   -- total 525 lines in a field, last 16.6425 ms
CONSTANT FRAME_LINES : integer := 480; -- line number in one field
CONSTANT TOTAL_LINES : integer := 525; -- line number in one field
       
SIGNAL l_count : integer := 0;      -- the number of lines has drawn
Signal  hcount : INTEGER := 0;       -- line pixel counter
constant  TAA :  time := 10ns;
constant TOHA : time := 3ns;

signal  rdata      : std_logic_vector (15 downto 0);

type mem is array(0 to 640) of std_logic_vector(3 downto 0);
signal r_array,g_array,b_array : mem;
attribute ramstyle : string;
attribute ramstyle of r_array, g_array, b_array: signal is "M4K";
------------------------------------------------------
------------------------------------------------------
Begin
RESET   <= SW(1);
VSYNC_O <= VSYNC;
HREF_O  <= HREF;
PCLK_O  <= PCLK;

SRAM_CE_N <= '0';
SRAM_UB_N <= '0';
SRAM_LB_N <= '0';

Address_Generator:   Process(PCLK)
---------------------------------------------------------------------------
Function yuvtorgb (signal  y1 : in std_logic_vector(7 downto 0);signal y2 : in std_logic_vector(7 downto 0);
			       signal   u : in std_logic_vector(7 downto 0);signal  v : in std_logic_vector(7 downto 0)) 
return std_logic_vector  is
	  variable   data_v   :   INTEGER; 
	  variable   data_y1  :   INTEGER; 
	  variable   data_u   :   INTEGER; 
	  variable   data_y2  :   INTEGER; 
	  variable   red      :   integer  range 0 to 255; 
	  variable   green    :   integer  range 0 to 255; 
	  variable   blue     :   integer  range 0 to 255; 
	  variable   rgb1     :   std_logic_vector (15 downto 0);
	begin
	  data_y1 := to_integer(unsigned(y1));
	  data_y2 := to_integer(unsigned(y2));
	  data_u  := to_integer(unsigned(u));
	  data_v  := to_integer(unsigned(v));
--------------------------------------------------------------------------
	  red   := data_y1 + 140*(data_u-128)/100;
	  green := data_y1 - 34 *(data_v-128)/100 -71*(data_u-128)/100;
	  blue  := data_y1 + 177*(data_v-128)/100;
	  
	  red   := red*15/255;
	  green := green*15/255;
	  blue  := blue*15/255;
	  
	  rgb1(3 downto 0)   := std_logic_vector(to_unsigned(red,4));
	  rgb1(7 downto 4)   := std_logic_vector(to_unsigned(green,4));
	  rgb1(11 downto 8)  := std_logic_vector(to_unsigned(blue,4));
	  rgb1(15 downto 12) := "0000";
--------------------------------------------------------------
      return rgb1;
end yuvtorgb;
--------------------------------------------------------------
Function ytorgb (signal  y: in std_logic_vector(7 downto 0)) 
return std_logic_vector  is
	  variable   data_y   :   INTEGER; 
	  variable   red      :   integer  range 0 to 255; 
	  variable   green    :   integer  range 0 to 255; 
	  variable   blue     :   integer  range 0 to 255; 
	  variable   rgb      :   std_logic_vector (15 downto 0);
begin
	  data_y := to_integer(unsigned(y));
-----------------------------------------------------------
	  red   := data_y*15/255;
	  green := data_y*15/255;
	  blue  := data_y*15/255;
	  
	  rgb(3 downto 0)   := std_logic_vector(to_unsigned(red,4));
	  rgb(7 downto 4)   := std_logic_vector(to_unsigned(green,4));
	  rgb(11 downto 8)  := std_logic_vector(to_unsigned(blue,4));
	  rgb(15 downto 12) := "0000";

      return rgb;
end ytorgb;
--------------------------------------------------------------
	variable  iaddr  : std_logic_vector (16 downto 0);
    variable  addr   : integer;
--------------------------------------------------------------
Begin                                          
 if (rising_edge(PCLK)) then
	If (RESET ='1') THEN 
		Address <= "000000000000000001";
		CMR_MEM_BUSY <= '0';
			
        cl_count <= 0;
        chcount  <= 0;
		    
	      Count    <= '0';
	    first_data <= '0'; 	
	else
	   if (VSYNC ='1' ) then   		-- start of a new field
		    Data1(15 downto 8) <=  Y;
		    Data1( 7 downto 0) <= UV;
			
		    Count    <= '0';
            cl_count <= 0;
            chcount  <= 0;
		    first_data <= '0'; 	
		  
		    CMR_MEM_BUSY <= '0';	
		    CMR_WE <= '1';
       else             
          if (FODD = '1' ) then    	-- even Field
	         if (HREF ='1') then
--------------------------------------------------------
		       if (first_data = '1') then  
				  chcount <= chcount +1;
		       else                	-- first pixel in a line
				  first_data <= '1';
				  chcount  <= 1;
				  cl_count <= cl_count +1;
		       end if;

			   if (chcount <= 640 and cl_count <= 240) then
	              if ( Count = '0') then 	---the first pixel
------------------------------------------------
				      addr  := (cl_count-1) *320 + chcount/2 + 1;
				      iaddr := std_logic_vector(to_unsigned(addr,17));

				      Address <= '0'&iaddr;
		
			          Count <= '1';
     
					  Data1(15 downto 8) <= Y;
	                  Data1(7 downto 0) <= UV;
					
					if ( sw(3) = '0') then
		              Data <= ytorgb(Y);
					else
---					  Data <= yuvtorgb(Data1(15 downto 8), Data2(15 downto 8),Data1(7 downto 0), Data2(7 downto 0) );
					end if;
------------------------------------------------	  
		              if (VGA_MEM_BUSY ='0') then
			              CMR_MEM_BUSY <= '1';	
			              CMR_WE <= '0';
			              CMR_RAM_DATA <= Data;
			              CMR_RAM_ADDR <= Address;
		              end if;
------------------------------------------------
	              else                        -- second pixel, discard
		               Count <= '0';
					   Data2(15 downto 8) <= Y;
	                   Data2(7 downto 0)  <= UV;
		               CMR_MEM_BUSY <= '0';	
	                   CMR_WE <= '1';
	              end if;    -- end of count if
				else 
		               CMR_MEM_BUSY <= '0';	
	                   CMR_WE <= '1';
				end if;		
	       else              -- href = 0
		       CMR_MEM_BUSY <= '0';	
	           CMR_WE <= '1';
                      
			   chcount  <= 0;
	           first_data <= '0'; 	
-----------------------------------------------------------------
           end if;    -- end of href
-----------------------------------------------------------------
        else     --  odd field    fodd is 0
		     CMR_MEM_BUSY <= '0';	
	         CMR_WE <= '1';
                 
             cl_count <= 0;
             chcount  <= 0;
 	         first_data <= '0'; 	
        end if;  -- end of fodd
       end if;   -- end of VSYNC
    end if;    -- end of reset
 end if;     -- end of pclk
End Process;


pixel_draw : PROCESS(CLOCK_25,RESET) -- drawing pixels and blank pulses
		variable  iaddr      : std_logic_vector (16 downto 0);
		variable  baddr1      : std_logic_vector (17 downto 0);
		variable  baddr2      : std_logic_vector (17 downto 0);
	    variable t_vgab      : std_logic_vector(3 downto 0);
	    variable t_vgar      : std_logic_vector(3 downto 0);
	    variable t_vgag      : std_logic_vector(3 downto 0);
		variable t_vga_addr  :  std_logic_vector (17 downto 0);
	    variable l_ext      : std_logic := '0';
   	    variable h_ext      : std_logic := '0';
	    variable addr : integer;
    BEGIN
       IF RESET= '1' THEN
          hcount <= 0;
          l_count <=  0 ;
          l_ext := '0';
          h_ext := '0';
          VGA_MEM_BUSY <= '0';
        ELSIF rising_edge(CLOCK_25) THEN
		  IF l_count < FRAME_LINES THEN
             if l_ext = '0'  then   -- first line 
                IF hcount < LINE_PIXELS THEN
                   if h_ext = '0' then   -- first pixel
					  addr  := l_count * 160 + hcount/2 + 1; 
					  iaddr := std_logic_vector(to_unsigned(addr,17));
					  baddr1 := '0'&iaddr;
					  baddr2 := '1'&iaddr;
-------------------------------------------------------------------------------					
					  if (CMR_MEM_BUSY = '0')then
						if (SW(0) = '0') then
					      VGA_MEM_BUSY <= '1';
						  VGA_WE <= '1';
					      VGA_RAM_ADDR <= baddr1;
				
					      t_vgar := VGA_RAM_DATA(3 downto 0);
					      t_vgag := VGA_RAM_DATA(7 downto 4);
					      t_vgab := VGA_RAM_DATA(11 downto 8);
					
					      t_vga_addr := baddr2 ;
					    else
					      VGA_MEM_BUSY <= '1';
						  VGA_WE  <= '1';
					      VGA_RAM_ADDR <= baddr2;
				
					      t_vgar := VGA_RAM_DATA(3 downto 0);
					      t_vgag := VGA_RAM_DATA(7 downto 4);
					      t_vgab := VGA_RAM_DATA(11 downto 8);
						END IF;
					 END IF;    -- end of CMR_MEM_BUSY
----------------------------------------------------------------------------------              
					 VGA_R <= t_vgar;
					 VGA_B <= t_vgab;
					 VGA_G <= t_vgag;

					 r_array(hcount) <= t_vgar;
					 g_array(hcount) <= t_vgag;
					 b_array(hcount) <= t_vgab;
                
					 hcount <= hcount+1;
					 h_ext := '1';
                   elsif h_ext = '1' then     ---  second pixel
					 VGA_R <= t_vgar;
					 VGA_B <= t_vgab;
					 VGA_G <= t_vgag;

					 if (SW(0) = '0') then
					  	VGA_WE <= '0';
 					    VGA_RAM_ADDR <= t_vga_addr;
		  			 end if;
				
					 r_array(hcount) <= t_vgar;
					 g_array(hcount) <= t_vgag;
					 b_array(hcount) <= t_vgab;

					 hcount <= hcount+1;
					 h_ext := '0';
					 VGA_MEM_BUSY <= '0';
			       END IF;                   ---  end of the h_ext
              ELSIF hcount >=LINE_PIXELS and hcount < LINE_PIXELS+HFP+HSYNC_TIME+HBP THEN
                VGA_R <= "0000";
                VGA_B <= "0000";
                VGA_G <= "0000";
                hcount <= hcount+1;
              ELSE
                hcount <= 0;
                VGA_R <= "0000";
                VGA_B <= "0000";
                VGA_G <= "0000";
                l_count <= l_count+1;
			    l_ext :='1';
              END IF;  ---  end of the hcount
			ELSif l_ext = '1'  then
                IF hcount < LINE_PIXELS THEN
					VGA_R <= r_array(hcount);
					VGA_B <= b_array(hcount);
					VGA_G <= g_array(hcount);

					hcount <= hcount+1;
					VGA_MEM_BUSY <= '0';
                 ELSIF hcount >=LINE_PIXELS and hcount < LINE_PIXELS+HFP+HSYNC_TIME+HBP THEN
                    VGA_R <= "0000";
                    VGA_B <= "0000";
                    VGA_G <= "0000";
                    hcount <= hcount+1;
                 ELSE
                    hcount <= 0;
                    VGA_R <= "0000";
                    VGA_B <= "0000";
                    VGA_G <= "0000";
                    l_count <= l_count+1;
			        l_ext :='0';
			     END IF;
			 END IF;  ---  end of the l_ext
          ELSIF (l_count >= FRAME_LINES and l_count < TOTAL_LINES) THEN
			IF hcount < LINE_PIXELS+HFP+HSYNC_TIME+HBP THEN
              VGA_R <= "0000";
              VGA_B <= "0000";
              VGA_G <= "0000";
              hcount <= hcount+1;
            ELSE
              hcount <= 0;
              VGA_R <= "0000";
              VGA_B <= "0000";
              VGA_G <= "0000";
              l_count <= l_count+1;
            END IF;
          ELSE
              VGA_R <= "0000";
              VGA_B <= "0000";
              VGA_G <= "0000";
              l_count <= 0;
          END IF; ---  end of the l_count
        END IF;  -- end of the clock_25
    END PROCESS;
    
hsyn : PROCESS(CLOCK_25)  -- horizontal syn
   BEGIN
		if rising_edge(CLOCK_25) then
			if (hcount >= LINE_PIXELS + HFP and hcount < LINE_PIXELS + HFP + HSYNC_TIME) then
				VGA_HS <= '0' ;
			else VGA_HS <= '1';
			end if;
		end if;
   END PROCESS;
   
vsyn : PROCESS(CLOCK_25)   -- vertical syn
   BEGIN
        IF rising_edge(CLOCK_25) THEN
            IF (l_count = FRAME_LINES +10 or l_count = FRAME_LINES +11) THEN
                   VGA_VS <= '0';
			ELSE   VGA_VS <= '1';
			END IF;
       END IF;
   END PROCESS;
   
clk_25 : PROCESS(CLOCK_50,RESET)    -- clock-25
       VARIABLE count : INTEGER := 0;
    BEGIN
       IF RESET= '1' THEN
          CLOCK_25 <= '0';
          count := 0;
       ELSIF rising_edge(CLOCK_50) THEN
          IF count = 0 THEN
              CLOCK_25 <= '1';  
              count := 1;
          ELSIF count = 1 THEN
              CLOCK_25 <= '0';  
              count := 0;
          END IF;
       END IF; 
    END PROCESS;

SRAM: process(VGA_RAM_ADDR,CMR_RAM_ADDR)
	begin
	  assert(SRAM_CE_N = '0');
	  assert(SRAM_UB_N = '0');
	  assert(SRAM_LB_N = '0');
	  
		  if CMR_WE = '0' then
			 SRAM_WE_N <= '0';
			 SRAM_OE_N <= '1';
		     SRAM_ADDR <= CMR_RAM_ADDR;
		     SRAM_DQ   <= CMR_RAM_DATA;
    	  elsif VGA_WE = '0' then
		     SRAM_WE_N <= '0';
		     SRAM_OE_N <= '1';
		     SRAM_ADDR <= VGA_RAM_ADDR;
		     SRAM_DQ   <= VGA_RAM_DATA;
	      else 
	         SRAM_OE_N <= '0';
			 SRAM_WE_N <= '1';
		     SRAM_DQ <= "ZZZZZZZZZZZZZZZZ";
	         SRAM_ADDR    <= VGA_RAM_ADDR;
		     VGA_RAM_DATA <= SRAM_DQ after 10ns; 
 	      end if;
	end process;
End behaviour;

-------------------------------------------------------------------------------------