"use strict";

function drawWTP(parameters){

    this.treatment=parameters.treatment
    this.bonusAmounts = parameters.bonusAmounts
    this.minBonus = parameters.minBonus
    this.maxBonus = parameters.maxBonus
    this.varname=parameters.varname
    this.root=parameters.root
    this.hidden_fields_name=parameters.hidden_fields_name
    this.playerID=parameters.playerID
    this.numForcedBoxed=parameters.numForcedBoxed
    this.answers = {}
    

    var modal_div=document.createElement("div");
    modal_div.innerHTML=`
    <div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="confirmModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-body" id="confirm_modal_text_id">
                <p class="pb-0 mb-0">Are you sure about your answers?</p>
            </div>
            <div class="modal-footer">
                <button type="button" data-bs-dismiss="modal" class="btn btn-secondary">Change answers</button>
                <button id="id_button_end_task" style="float: right" class="btn btn-primary btn-large">Confirm</button>
            </div>
            </div>
        </div>
    </div>`


    document.getElementById(this.root).appendChild(modal_div);


    this.drawQuestions = function(base){
        for (let i = 0; i < this.bonusAmounts.length; i++) {
            console.log("Index:", i, "Value:", this.bonusAmounts[i]);
            var div = document.createElement("div");
            base.appendChild(div);
            var p = document.createElement("h3");
            p.innerHTML = "Question " + String(i + 1);
        
            div.appendChild(p);

            var p = document.createElement("p");
            p.className = "text-center pb-2 mb-0";
            if (this.treatment == "bonus") {

                p.innerHTML = "Do you want to open "+this.numForcedBoxed+" boxes (bonus between $"+this.minBonus + " and $"+this.maxBonus+") or do you want a bonus of $" + this.bonusAmounts[i] + " for sure?";
            } else {
                p.innerHTML = "Do you want to open "+this.numForcedBoxed+" boxes (penalty between $"+this.minBonus + " and $"+this.maxBonus+") or do you want a penalty of $" + String(this.maxBonus + this.minBonus - this.bonusAmounts[i]) + " for sure?";
            };
            div.appendChild(p);
            
            var div2 = document.createElement("div");
            div2.className = "d-flex justify-content-around";

            div.appendChild(div2);

            var taskButton=document.createElement("button")
            taskButton.setAttribute("type","button");
            taskButton.setAttribute("id","taskButton_id_"+String(i));
            taskButton.className="btn btn-sm btn-secondary";
            if (this.treatment == "bonus") {
                    taskButton.innerHTML="Open "+this.numForcedBoxed + " boxes and look for best bonus";
            }  else {
                    taskButton.innerHTML="Open "+this.numForcedBoxed + " boxes and look for best penalty";
            }
            taskButton.style.width = "300px";


            
            taskButton.addEventListener('click', () => {
                document.getElementById("taskButton_id_"+String(i)).classList.remove("btn-success");
                document.getElementById("sureBonusButton_id_"+String(i)).classList.remove("btn-success");
                document.getElementById("taskButton_id_"+String(i)).classList.add("btn-success");
                this.answers[this.bonusAmounts[i]] = "task";
                if (Object.keys(this.answers).length == this.bonusAmounts.length) {
                    document.getElementById("next_button_id_de").style.display = "";   
                    document.getElementById(this.varname).value=JSON.stringify(this.answers);

                }
            });
            div2.appendChild(taskButton);


            var sureBonusButton=document.createElement("button")
            sureBonusButton.setAttribute("type","button");
            sureBonusButton.setAttribute("id","sureBonusButton_id_"+String(i));
            sureBonusButton.className="btn btn-sm btn-secondary";
            if (this.treatment == "bonus") {
                sureBonusButton.innerHTML="Get $"+this.bonusAmounts[i] + " bonus for sure";
            }  else {
                sureBonusButton.innerHTML="Get $"+String(this.maxBonus + this.minBonus - this.bonusAmounts[i]) + " penalty for sure";
            }
            sureBonusButton.style.width = "300px";
            sureBonusButton.addEventListener('click', () => {
                document.getElementById("taskButton_id_"+String(i)).classList.remove("btn-success");
                document.getElementById("sureBonusButton_id_"+String(i)).classList.remove("btn-success");
                document.getElementById("sureBonusButton_id_"+String(i)).classList.add("btn-success");
                this.answers[this.bonusAmounts[i]] = "sure";
                if (Object.keys(this.answers).length == this.bonusAmounts.length) {
                    document.getElementById("next_button_id_de").style.display = "";   
                    document.getElementById(this.varname).value=JSON.stringify(this.answers);

                }
                

            
            });
            div2.appendChild(sureBonusButton);

            var hr = document.createElement("hr");
            div.appendChild(hr);
 



          }
        

    }

    this.drawQuestions(document.getElementById(this.root));




    


    this.showNext=function(){
        var nextButton=document.getElementById("id_next_button");
        if (nextButton){
            nextButton.style.display="";
        }
    }
    
    


    var hiddenDiv = document.getElementById(this.hidden_fields_name);
    var hiddenField=document.createElement("input");
    hiddenDiv.appendChild(hiddenField);
    hiddenField.setAttribute("type","hidden");
    hiddenField.setAttribute("name",this.varname);
    hiddenField.setAttribute("id",this.varname); 

    // //draw game  
    // var container=document.createElement("div");
    // container.className="container";
    // document.getElementById(this.root).appendChild(container);
    // var row=document.createElement("div");
    // row.className="row";
    // container.appendChild(row);
    // this.leftDiv=document.createElement("div");
    // this.leftDiv.className="col-2 px-0";
    // this.leftDiv.innerHTML="&nbsp;";
    // row.appendChild(this.leftDiv);
    // this.midDiv=document.createElement("div");
    // this.midDiv.className="col-8 px-0 mx-0";
    // row.appendChild(this.midDiv);
    // this.rightDiv=document.createElement("div");
    // this.rightDiv.className="col-2 px-0";
    // this.rightDiv.innerHTML="&nbsp;";
    // row.appendChild(this.rightDiv);
    // // this.drawChoices(this.midDiv,this.leftHeader,this.rightHeader,this.leftBonus,this.rightBonus);
    // this.load();




}



