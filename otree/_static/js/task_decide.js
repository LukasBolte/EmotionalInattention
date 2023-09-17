"use strict";

function task(parameters){
    
    //fundamentals (coming from outside)
    this.playerID=parameters.playerID;
    console.log(parameters.root)
    this.root=document.getElementById(parameters.root);
    console.log("my highlighting")
    console.log(this.root,"my root element")
    
    this.varname=parameters.varname;
    this.sequence=JSON.parse(parameters.sequence);
    this.min_pay=parseInt(parameters.min_pay);
    this.max_pay=parseInt(parameters.max_pay);
    this.treatment=parameters.treatment;
    this.delay=parameters.delay;
    this.open_box_src=parameters.open_box_src;
    this.closed_box_src=parameters.closed_box_src;

    console.log(parameters, 'my parameters')
    this.draw=function(){
        //attach input field
        var hidden=document.createElement("input");
        hidden.setAttribute("type","hidden");
        hidden.setAttribute("id",this.varname);
        hidden.setAttribute("name",this.varname);
        this.root.appendChild(hidden);

        
        var modal_div=document.createElement("div");
        modal_div.innerHTML=`
        <div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="confirmModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-body">
                    <p class="pb-0 mb-0">Are you sure you want to end the task? You will not be able to return and open more boxes.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" data-bs-dismiss="modal" class="btn btn-primary">Back to task</button>
                    <button id="id_button_end_task" style="float: right" class="btn btn-secondary btn-large">End task</button>
                </div>
                </div>
            </div>
        </div>`


        
        this.root.appendChild(modal_div);
        document.getElementById("id_button_end_task").addEventListener('click', () => {
            this.draw3();
            });


        //attach container that can easily be reset
        var container=document.createElement("div");

        // container.setAttribute("id","container_id");
        this.root.appendChild(container);

        var div=document.createElement("div");
        div.className="row justify-content-center";
        container.appendChild(div);

        var divWidth=document.createElement("div");
        divWidth.className="col-md-6 col-lg-9";

        div.appendChild(divWidth)
        this.container = divWidth
    };

    this.drawBox=function(){
        var table=document.createElement("table");
        table.className="table no-border-table";
        this.container.appendChild(table);

        var tbody=document.createElement("tbody");
        table.appendChild(tbody);

        var tr=document.createElement("tr")
        tr.style.height = '222px'
        tbody.appendChild(tr);

        var td=document.createElement("td")
        td.setAttribute("id","row1_id")
        td.className="col-6";
        td.style.textAlign='center';
        tr.appendChild(td);

        var tr=document.createElement("tr")
        tr.style.height = '100px'
        tbody.appendChild(tr);

        var td=document.createElement("td")
        td.setAttribute("id","row2_id");
        td.style.textAlign='center';
        tr.appendChild(td);
    };

    this.load=function(){
        var keyName=this.playerID+":"+this.root;
        var savedValue=localStorage.getItem(keyName); 
        console.log(savedValue);
        this.num_draws=0;
        this.tentative_bonus=this.min_pay;
        this.tentative_bonus_sequence=[];
        this.open_page="page1";
        if (savedValue!=undefined){
            this.num_draws=JSON.parse(savedValue)['num_draws'];
            this.open_page=JSON.parse(savedValue)['open_page'];
            this.tentative_bonus=JSON.parse(savedValue)['tentative_bonus'];
            this.tentative_bonus_sequence=JSON.parse(savedValue)['tentative_bonus_sequence'];
        }
        var output={};
        output.num_draws=this.num_draws;
        output.open_page=this.open_page;
        output.tentative_bonus=this.tentative_bonus;
        output.tentative_bonus_sequence=this.tentative_bonus_sequence;
        document.getElementById(this.varname).value=JSON.stringify(output);
    };

     //storage functions
    this.save=function(){
        var keyName=this.playerID+":"+this.root;
        var output={};
        output.num_draws=this.num_draws;
        output.open_page=this.open_page;
        output.tentative_bonus=this.tentative_bonus;
        output.tentative_bonus_sequence=this.tentative_bonus_sequence;
        localStorage.setItem(keyName,JSON.stringify(output));
        document.getElementById(this.varname).value=JSON.stringify(output);
    }

    this.clearContainer=function(){
        this.container.innerHTML="";
    };

    this.draw1=function(){
        this.clearContainer();
        this.drawBox();
        var td=document.getElementById("row1_id");

        var container=document.createElement("div");
        td.appendChild(container);
        
        var table=document.createElement("table");
        table.className="table no-border-table";
        container.appendChild(table)
        var tbody=document.createElement("tbody");
        table.appendChild(tbody)
        var tr=document.createElement("tr")
        tbody.append(tr);
        var td1=document.createElement("td");
        td1.style.width="50%";

        var p=document.createElement('p');
        var bonus
        if (this.num_draws==0){
            bonus=this.min_pay;
        } else {
            bonus=Math.max(...this.sequence.slice(0,this.num_draws))
        }

        var amount
        if (this.treatment=="bonus"){
            p.innerHTML="Your final tentative bonus if you end the task now:"
            amount = bonus
        } else if (this.treatment=="penalty"){
            p.innerHTML="Your final tentative penalty if you end the task now:"
            amount = this.min_pay+this.max_pay-bonus
        }

        

        
        td1.appendChild(p);


        var p=document.createElement('p');
        p.className="h3 mt-5";
        p.innerHTML="$"+ amount.toFixed(2);

        td1.appendChild(p);
        tr.appendChild(td1)



        var td2=document.createElement("td");
        td2.style.width="50%";

        

        var p=document.createElement('p');
        p.innerHTML="Next box:"
        td2.appendChild(p);
        var img=document.createElement('img');
        img.setAttribute("src",this.closed_box_src)
        img.className="img-fluid mb-3";
        img.style.height="100px";
        td2.appendChild(img);



        tr.appendChild(td2)
        
        var td=document.getElementById("row2_id");




        var container=document.createElement("div");
        td.appendChild(container);
        
        var table=document.createElement("table");
        table.className="table no-border-table";
        container.appendChild(table)
        var tbody=document.createElement("tbody");
        table.appendChild(tbody)
        var tr=document.createElement("tr")
        tbody.append(tr);
        var td0=document.createElement("td")
        td0.style.width="50%";
        tr.appendChild(td0)
        var td1=document.createElement("td");
        td1.style.width="25%";
        td1.className="no-padding";

        var openBoxButton=document.createElement("button")
        openBoxButton.setAttribute("type","button");
        openBoxButton.setAttribute("id","openBoxButton_id")
        openBoxButton.className="btn btn-primary";
        openBoxButton.innerHTML="Open box ("+this.delay+"s)";
        openBoxButton.addEventListener('click', () => {
            document.getElementById("openBoxButton_id").disabled = true;
            this.startOpening();
          });
        td1.appendChild(openBoxButton);

        tr.appendChild(td1)

        var td2=document.createElement("td");
        td2.style.width="25%";
        td2.className="no-padding";

        var endTaskButton=document.createElement("button")
        endTaskButton.setAttribute("type","button");
        endTaskButton.className="btn btn-secondary";
        endTaskButton.innerHTML="End task";

        endTaskButton.setAttribute("data-bs-toggle","modal");
        endTaskButton.setAttribute("data-bs-target","#confirmModal");
        
        
        td2.appendChild(endTaskButton);

        tr.appendChild(td2)  
    }

    this.formatNumberOrString=function(last_num) {
        if (typeof last_num === 'number' || !isNaN(last_num)) {
          // If last_num is a number or can be converted to a number, treat it as a number
          return parseFloat(last_num).toFixed(2);
        } else {
          // Otherwise, treat it as an initial string and try to convert it to a number
          const parsedNum = parseFloat(last_num);
          if (!isNaN(parsedNum)) {
            // If parsedNum is a valid number, convert it to a fixed format
            return parsedNum.toFixed(2);
          } else {
            // If parsedNum is NaN (Not-a-Number), return the original string as is
            return last_num;
          }
        }
      }

    this.startOpening=function(){
        console.log(this.delay)
        let seconds =this.delay-1;
        document.getElementById("openBoxButton_id").innerHTML="Open box ("+seconds.toString()+"s)"
        // Update the timer every second
        const timerInterval = setInterval(() => {
            // Decrease the seconds by 1
          seconds--;
          console.log(seconds);
          document.getElementById("openBoxButton_id").innerHTML="Open box ("+seconds.toString()+"s)"
  
          
  
          // Check if the timer has reached zero
          if (seconds ===  -1) {
            clearInterval(timerInterval); // Stop the timer
            this.num_draws++;
            this.open_page="page2";

            console.log(this, 'my second this element')

            this.save();

            this.draw2(); // Call the function after the timer reaches zero
          }
        }, 1000); // Interval of 1 second (1000 milliseconds)
    }
    
    this.draw2=function(){
        this.clearContainer();
        // clearInterval(timerInterval)
        console.log("draw2 is executed")
        this.drawBox();
        var td=document.getElementById("row1_id");
        var p=document.createElement('p');
        p.innerHTML="You decided to open the box"
        td.appendChild(p);
        var img=document.createElement('img');
        img.setAttribute("src",this.open_box_src)
        img.className="img-fluid mb-3";
        img.style.height="70px";
        td.appendChild(img);
    
        console.log(this.num_draws,'number of draws heeeere')
        console.log(this.sequence, this.num_draws-1)
        var last_num= this.sequence[this.num_draws-1]
   
        console.log(last_num, 'last number')
        console.log(typeof(last_num), 'last number type')
        var p=document.createElement('p');
        if (this.treatment=="bonus"){
            p.innerHTML="The box contains a bonus amount of <b>$"+this.formatNumberOrString(last_num)+"</b>"
        } else if (this.treatment=="penalty"){
            var penalty = this.min_pay+this.max_pay-last_num
            p.innerHTML="The box contains a penalty amount of <b>$"+this.formatNumberOrString(penalty)+"</b>"
        }

        
        td.appendChild(p);

        var p=document.createElement('p');
        
        if (this.treatment=="bonus"){
            p.innerHTML="Your current tentative bonus is <b>$"+ this.formatNumberOrString(this.tentative_bonus) + '</b>. Do you want to keep your tenatitve bonus or replace it with the bonus amount inside the box?'
        } else if (this.treatment=="penalty"){
            var penalty = this.min_pay+this.max_pay-last_num
            p.innerHTML="Your current tentative penalty is <b>$"+ this.formatNumberOrString(penalty) + '</b>. Do you want to keep your tenatitve penalty or replace it with the penalty amount inside the box?'
        };

        td.appendChild(p);

        var p=document.createElement('p');
        p.className="d-flex justify-content-around";
        
        // keep button
        var keepButton=document.createElement("button")
        keepButton.setAttribute("type","button");
        keepButton.setAttribute("id","keepButton_id")
        keepButton.className="btn btn-secondary btn-sm";
        keepButton.innerHTML="Keep";
        keepButton.addEventListener('click', () => {
            document.getElementById("continueButton_id").style.visibility = "visible";
            var element = document.getElementById("endPratice_text_id");
            if (element) {
                element.style.visibility = "visible";
            };
            document.getElementById("keepButton_id").classList.remove("btn-secondary");
            document.getElementById("keepButton_id").classList.add("btn-success");

            document.getElementById("replaceButton_id").classList.remove("btn-success");
            document.getElementById("replaceButton_id").classList.add("btn-secondary");

        //  this.open_page="page1";
        //  this.save()
        //  this.draw1();
        });
        p.appendChild(keepButton);

        // keep button
        var replaceButton=document.createElement("button")
        replaceButton.setAttribute("type","button");
        replaceButton.setAttribute("id","replaceButton_id")
        replaceButton.className="btn btn-secondary btn-sm";
        replaceButton.innerHTML="Replace";
        replaceButton.addEventListener('click', () => {
            document.getElementById("continueButton_id").style.visibility = "visible";
            var element = document.getElementById("endPratice_text_id");
            if (element) {
                element.style.visibility = "visible";
            };
            

            document.getElementById("replaceButton_id").classList.remove("btn-secondary");
            document.getElementById("replaceButton_id").classList.add("btn-success");

            document.getElementById("keepButton_id").classList.remove("btn-success");
            document.getElementById("keepButton_id").classList.add("btn-secondary");

            this.tentative_bonus=last_num;
        //  this.open_page="page1";
        //  this.save()
        //  this.draw1();
        });

        p.appendChild(replaceButton);
        
        td.appendChild(p);

        console.log('toward the end')
        var td=document.getElementById("row2_id");

        // continue button
        var continueButton=document.createElement("button")
        continueButton.setAttribute("type","button");
        continueButton.setAttribute("id","continueButton_id")
        continueButton.className="btn btn-primary";
        continueButton.style="visibility: hidden;"
        continueButton.innerHTML="Continue";
        continueButton.addEventListener('click', () => {
            this.open_page="page1";
            this.tentative_bonus_sequence.push(this.tentative_bonus);
            this.save()
            this.draw1();
        });


        td.appendChild(continueButton);


        // var p=document.createElement('p');
        // var bonus=Math.max(...this.sequence.slice(0,this.num_draws))
   
        // if (this.treatment=="bonus"){
        //     p.innerHTML="So your bonus if you end the task now is $"+ this.formatNumberOrString(bonus)
        // } else if (this.treatment=="penalty"){
        //     var penalty = this.min_pay+this.max_pay-bonus
        //     p.innerHTML="So your penalty if you end the task now is $"+ this.formatNumberOrString(penalty)
        // }

        
        // td.appendChild(p);
        
 
    }
    

    this.draw3=function(){
        this.clearContainer();
        console.log("draw3 is executed")
        this.drawBox();
        var td=document.getElementById("row1_id");
        var p=document.createElement('p');
        p.innerHTML="You decided to end the task"
        td.appendChild(p);
        
        var p=document.createElement('p');

        var bonus
        if (this.num_draws==0){
            bonus=this.min_pay;
        } else {
            bonus=Math.max(...this.sequence.slice(0,this.num_draws))
        }

       
        if (this.treatment=="bonus"){
            p.innerHTML="Your final bonus is $"+ this.formatNumberOrString(bonus)
        } else if (this.treatment=="penalty"){
            var penalty = this.min_pay+this.max_pay-bonus
            p.innerHTML="Your final penalty is $"+this.formatNumberOrString(penalty)
        }

            
        td.appendChild(p);

        var td=document.getElementById("row2_id");

        var nextButton=document.createElement("button")
        nextButton.setAttribute("id","nextButton_id")
        nextButton.className="btn btn-primary btn-large";
        nextButton.innerHTML="Next";
        nextButton.style.float = 'right';
        td.appendChild(nextButton);

        // <button style="float: right" class="btn btn-primary btn-large">Next</button>
        this.save();
    }



    this.draw();
    this.load();

    switch (this.open_page) {
        case "page1":
            this.draw1();
            break;
        case "page2":
            this.draw2();
            break;
        case "page3":
            this.draw3();
            break;
        }

}

