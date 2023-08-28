"use strict";

function drawWTP(parameters){
    this.leftHeader=parameters.leftHeader
    this.rightHeader=parameters.rightHeader
    this.leftBonus=parameters.leftBonus
    this.rightBonus=parameters.rightBonus
    this.varname=parameters.varname
    this.root=parameters.root
    this.color_switched=parameters.color_switched
    this.hidden_fields_name=parameters.hidden_fields_name
    this.playerID=parameters.playerID
    this.tdList={};
    this.selectedCutoff;
    this.cutoffHistory=[];

    this.leftDiv;
    this.rightDiv;


    this.drawChoices = function(base,leftHeader,rightHeader,leftBonus,rightBonus){
        var table=document.createElement("table");
        table.setAttribute("id","id_"+this.varname)
        table.className="table table-hover";
        table.style.backgroundColor = 'navajowhite';
        table.style.pointerEvents = '';
        base.appendChild(table);
        //add header
        var thead=document.createElement("thead");
        table.appendChild(thead);
        var trHead=document.createElement("tr");
        thead.appendChild(trHead);
        //now column headers
        var thHead=document.createElement("th");
        thHead.className="text-center";
        thHead.setAttribute("scope","col");
        thHead.style.width="35%";
        var text=document.createTextNode(leftHeader);
        thHead.appendChild(text);
        trHead.appendChild(thHead);
        
        var thHead=document.createElement("th");
        thHead.setAttribute("scope","col");
        thHead.style.width="20%";
        trHead.appendChild(thHead);

        var thHead=document.createElement("th");
        thHead.setAttribute("scope","col");
        var text=document.createTextNode(rightHeader);
        thHead.appendChild(text);
        thHead.className="text-center";
        thHead.style.width="35%";
        trHead.appendChild(thHead);
        //create body
        var tbody=document.createElement("tbody");
        tbody.addEventListener("mouseleave", this.unhighlight.bind(this));
        table.appendChild(tbody);
        var counter=0;
        for(let i=0;i<leftBonus.length;i++){
            var tr=document.createElement("tr");
            this.tdList[i]=[];
            tbody.appendChild(tr);
            //left choice
            var td=document.createElement("td");
            td.className="text-center";
            var text=document.createTextNode(leftBonus[i]);
            td.appendChild(text);
            td.setAttribute("cutoff","left:"+i);
            tr.appendChild(td);
            this.tdList[i].push(td);
            td.addEventListener("click", this.selectCutoff.bind(this));
            td.addEventListener("mouseenter", this.highlightSelection.bind(this));
            //middle OR
            var td=document.createElement("td");
            td.className="text-center";
            text=document.createTextNode("OR");
            td.setAttribute("cutoff","middle:"+i);
            td.appendChild(text);
            tr.appendChild(td);
            td.addEventListener("mouseenter", this.highlightSelection.bind(this));
            //right choice
            var td=document.createElement("td");
            td.className="text-center";
            text=document.createTextNode(rightBonus[i]);
            td.appendChild(text);
            td.setAttribute("cutoff","right:"+i);
            tr.appendChild(td);        
            this.tdList[i].push(td);
            td.addEventListener("click", this.selectCutoff.bind(this));
            td.addEventListener("mouseenter", this.highlightSelection.bind(this));
            counter++;
        }
    }


    this.highlight = function(cutoff,color){
        var choiceFrags=cutoff.split(':');
        var cutoffNum=parseFloat(choiceFrags[1]);
        for(var c in this.tdList){
            var cf=parseFloat(c);
            $(this.tdList[c][0]).removeClass("orange");
            $(this.tdList[c][0]).removeClass("darkorange");
            $(this.tdList[c][1]).removeClass("orange");
            $(this.tdList[c][1]).removeClass("darkorange");
            var color_dummy = 0;
            if (this.color_switched) {
                color_dummy = 1;
                console.log('color switched')
            };

            if (cf<cutoffNum){
                $(this.tdList[c][color_dummy]).addClass(color);
            }
            if (cf>cutoffNum){
                $(this.tdList[c][1-color_dummy]).addClass(color);
            }
            if (cf==cutoffNum){
                switch(choiceFrags[0]){
                    case "left":
                        $(this.tdList[c][0]).addClass(color);
                        break;
                    case "middle":
                        break;
                    case "right":
                        $(this.tdList[c][1]).addClass(color);
                        break;
                }
            }
        }    
    }
    
    this.unhighlight = function(){
        if (this.selectedCutoff){
            return;
        }
        for(var c in this.tdList){
            $(this.tdList[c][0]).removeClass("orange");
            $(this.tdList[c][1]).removeClass("orange");
            $(this.tdList[c][0]).removeClass("darkorange");
            $(this.tdList[c][1]).removeClass("darkorange");
        }
    }
    
    this.showNext=function(){
        var nextButton=document.getElementById("id_next_button");
        if (nextButton){
            nextButton.style.display="";
        }
    }
    
    this.selectCutoff = function(e){
        if (this.selectedCutoff){
            this.cutoffHistory.push(this.selectedCutoff);
        }
        var cutoff=e.target.getAttribute("cutoff");
        this.selectedCutoff=cutoff;
        this.highlight(cutoff,"darkorange");
        //save data in hidden field
        document.getElementById(this.varname).value=JSON.stringify({"history":this.cutoffHistory,"cutoff":this.selectedCutoff});   
        
        var keyName=this.playerID+":"+this.root+":"+this.varname;
        localStorage.setItem(keyName,JSON.stringify({"history":this.cutoffHistory,"cutoff":this.selectedCutoff}));
        console.log(document.getElementById(this.varname).value);  
        //make the oTree next button appear if present
        setTimeout(this.showNext,2000);
    }
    
    this.highlightSelection = function(e){
        e.target.style.cursor = "pointer";
        if (this.selectedCutoff){
            return;
        }
        var cutoff=e.target.getAttribute("cutoff");
        this.highlight(cutoff,"orange");
    }



    //// starting
    //storage functions
    this.load=function(){
        console.log('I am loading')
        var keyName=this.playerID+":"+this.root+":"+this.varname;
        var savedValue=localStorage.getItem(keyName); 
        //console.log(savedValue);
        if (savedValue!=undefined){
            var output=JSON.parse(savedValue);
            this.selectedCutoff = output["cutoff"]
            this.cutoffHistory = output["history"]
            console.log(this.selectedCutoff)
            this.highlight(this.selectedCutoff,"darkorange");
            document.getElementById(this.varname).value=JSON.stringify({"history":this.cutoffHistory,"cutoff":this.selectedCutoff});   
        }
    }
    //// ending


    var hiddenDiv = document.getElementById(this.hidden_fields_name);
    var hiddenField=document.createElement("input");
    hiddenDiv.appendChild(hiddenField);
    hiddenField.setAttribute("type","hidden");
    hiddenField.setAttribute("name",this.varname);
    hiddenField.setAttribute("id",this.varname); 
    //draw game  
    var container=document.createElement("div");
    container.className="container";
    document.getElementById(this.root).appendChild(container);
    var row=document.createElement("div");
    row.className="row";
    container.appendChild(row);
    this.leftDiv=document.createElement("div");
    this.leftDiv.className="col-2";
    this.leftDiv.innerHTML="&nbsp;";
    row.appendChild(this.leftDiv);
    var midDiv=document.createElement("div");
    midDiv.className="col-8";
    row.appendChild(midDiv);
    this.rightDiv=document.createElement("div");
    this.rightDiv.className="col-2";
    this.rightDiv.innerHTML="&nbsp;";
    row.appendChild(this.rightDiv);
    this.drawChoices(midDiv,this.leftHeader,this.rightHeader,this.leftBonus,this.rightBonus);

    this.load();
}
