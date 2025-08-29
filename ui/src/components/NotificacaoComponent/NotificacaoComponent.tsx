import { useState } from "react"
import { v4 as uuidv4 } from 'uuid';
import type { Message } from "./NotificacaoComponent.types";
import { api } from "../../utils/axios";

function NotificacaoComponent() {

  const [text, setText] = useState("")
  const [textHistory, setTextHistory] = useState<Message[]>([])

  
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event?.preventDefault()
    try{
      const idUnico = uuidv4();
      const formatedText = {
        notification: text,
        uuid: idUnico
      }
      const response = await api.post("/api/notificacoes", formatedText)
      console.log(response)
      setTextHistory([...textHistory, formatedText])
      console.log([...textHistory, formatedText])
    } catch (err) {
      console.log(err)
    }
  }




  return (
    <div>
      <form action="" onSubmit={handleSubmit}>
        <div>
          <input type="text" value={text} onChange={({target}) => setText(target.value)} placeholder="Digite uma mensagem"/>
        </div>
        <button type="submit">Enviar Notificação</button>
      </form>
      <div>
        <h1>Mensagens enviadas</h1>
        <ul style={{listStyle: "none"}}>
          {textHistory.map((message) => (
            <li key={message.uuid}>
              <p>{message.notification}</p>
            </li>
          ))}
        </ul>
      </div>
      
    </div>
  )
}

export default NotificacaoComponent
