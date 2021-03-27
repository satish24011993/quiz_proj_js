console.log('hello world quiz')
const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
//const timeBox = document.getElementsById('time-box')

// function begin001() {
//     c = 20;

// }

$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function (response) {
        // console.log(response)
        data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer =>
                    quizBox.innerHTML += `
                    <div>
                        <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                        <label for="${question}">${answer}</label>
                    </div>
                    `
                )
            }
        });
    },
    error: function(error){
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
            console.log(el.value)
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function (response){
            // console.log(response)
            const results = response.results
            console.log(results)
            quizForm.classList.add('not-visible')

            scoreBox.innerHTML = `${response.passed ? 'Congratulations! ' : 'Ops..: '}Your result is ${response.score.toFixed(2)}%`
            // const now = new Date().getTime()
            // console.log(now)
            //const time = response.time
            //console.log(time)
            //timeBox.innerHTML = `${time}`

            results.forEach(res => {
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)){
                    // console.log(question)
                    // console.log(resp)
                    // console.log('*****')

                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-light', 'h6']
                    resDiv.classList.add(...cls)

                    if (resp == 'not answered') {
                        resDiv.innerHTML += '- not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer: ${correct}`
                            resDiv.innerHTML += ` | answered: ${answer}`
                        }
                    }
                }
            const body = document.getElementsByTagName('BODY')[0]
            body.append(resDiv)
            })
        },
        error: function (error) {
            console.log(error)
        }
    })

}

// document.quizForm.onclick = function(){
//     var radVal = document.quizForm.rads.value;
//     result.innerHTML = 'You selected: '+radVal;
// }

quizForm.addEventListener('submit', e => {
    e.preventDefault()

    sendData()
})

// function timer001() {
//     c = c - 1;
//     if (c < 20) {
//         time001.innerHTML = c;
//     }

//     if (c < 1) {
//         window.clearInterval(update);
//         message001.innerHTML = "Time's Up";
//     }
// }

// update = setInterval("timer001()", 1000);

// function repeat001() {
//     location.reload();
// }