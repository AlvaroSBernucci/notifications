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
        mensagemId: idUnico,
        notification: text,
      }
      const response = await api.post("/api/notificacoes", formatedText)
      console.log(response.data)
      setTextHistory([...textHistory, response.data])
    } catch (err) {
      console.log(err)
    }
  }




  return (
    <div>
      <h1>Mensagens enviadas</h1>
      <form action="" onSubmit={handleSubmit}>
        <div style={{marginBottom: "10px"}}>
          <input type="text" value={text} onChange={({target}) => setText(target.value)} placeholder="Digite uma mensagem"/>
        </div>
        <button type="submit">Enviar Notificação</button>
      </form>
      <div>
        <ul style={{listStyle: "none"}}>
          {textHistory.map((message) => (
            <li key={message.mensagemId}>
              <p>Mensagem: {message.notification} - Status de envio: {message.status}</p>
            </li>
          ))}
        </ul>
      </div>
      
    </div>
  )
}

export default NotificacaoComponent
