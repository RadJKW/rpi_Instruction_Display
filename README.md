# rpi_Instruction_Display
Middle man to recieve UART messages from Z80 computer and then open web-svr pdf viewer
TASKS:
  • Handle Codes:
        All codes are transmitted in ASCII and are ended with a <CR> Carriage Return character (0A hex).

        GENERAL CODES:
        CI		Coil Information, followed by the 13-digit coil number and the division the coil is for.
            Sent on boot-up if there is an active coil.
            Format:  CI,nnnnnnnnnnnnn,n
            Example:  CI,0050123456789,1
        NC		New Coil, followed by the 13-digit coil number and the division the coil is for.
            Sent when a new coil spec is downloaded or winding is started on a new coil.
            Format:  NC,nnnnnnnnnnnnn,n
            Example:  NC,0050123456789,3
        NW		New Winding, followed by winding type, material type, and conductor width.
            Sent when a new winding is started.
            Format:  NW,XX,XX,nn.nnnn
        where winding type is PA (Paper), LV (Low Voltage), or HV (High Voltage)
        and material type is PM (Paper), WC (Wire), or SC (Sheet)
            Example:  NW,HV,WC,00.1250
        RS		Run Screen, followed by winding type, material type, and conductor width.
            Sent when the operator changes to the Run Screen.
            Format:  RS,XX,XX,nn.nnnn
              where winding type is PA (Paper), LV (Low Voltage), or HV (High Voltage)
              and material type is PM (Paper), WC (Wire), or SC (Sheet)
            Example:  RS,LV,SC,08.2500
        DE		Data Entry screen.  Sent when the operator changes to the winding data screen.
        FC		Finished Coil.  Sent when a coil is completed.

        “ALMOST” TURN STOPS:
        AAD		Almost at an Annular Duct stop
        ACX		Almost at a Crepe Extension Paper stop
        ADS		Almost at an End Duct stop
        ALE		Almost at a Layer End/End of Layer stop
        APX		Almost at a Plain Extension Paper stop
        ATB		Almost at a Tab Break/Section Break stop
        ATS		Almost at a Tap stop
        ATT		Almost at a Total Turns stop
        AXP		Almost at an Extra Paper stop
        TURN STOPS:
        AD		Annular Duct stop
        CX		Crepe Extension Paper stop
        DS		End Duct stop
        LE		Layer End/End of Layer stop
        PX		Plain Extension Paper stop
        TB		Tab Break/Section Break stop
        TS		Tap stop
        TT		Total Turns stop
        XP		Extra Paper stop
