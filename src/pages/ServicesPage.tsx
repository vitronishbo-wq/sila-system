import { useEffect, useState } from "react"
import { getServices } from "../services/serviceApi"
import {
  attachDocuments,
  createOrder,
  getReceipt,
  submitOrder
} from "../services/orderApi"
import { confirmPayment, generatePayment } from "../services/paymentApi"
import { DocumentPayload, ReceiptResponse, Service } from "../types/api"

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([])
  const [documents, setDocuments] = useState<DocumentPayload[]>([])
  const [isPreparingDocs, setIsPreparingDocs] = useState(false)
  const [docsError, setDocsError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [paymentReference, setPaymentReference] = useState<string | null>(null)
  const [receipt, setReceipt] = useState<ReceiptResponse | null>(null)

  useEffect(() => {
    loadServices()
  }, [])

  const loadServices = async () => {
    const data = await getServices()
    setServices(data)
  }

  const fileToDocumentPayload = (file: File): Promise<DocumentPayload> =>
    new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onerror = () => reject(new Error("Falha ao ler o arquivo."))
      reader.onload = () => {
        const uri = typeof reader.result === "string" ? reader.result : ""

        if (!uri) {
          reject(new Error("Falha ao gerar URI do documento."))
          return
        }

        resolve({
          filename: file.name,
          content_type: file.type || "application/octet-stream",
          size_bytes: file.size,
          uri
        })
      }
      reader.readAsDataURL(file)
    })

  const handleFileSelection = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const fileList = event.target.files

    if (!fileList || fileList.length === 0) {
      return
    }

    setDocsError(null)
    setIsPreparingDocs(true)

    try {
      const files = Array.from(fileList)
      const payloads = await Promise.all(files.map(fileToDocumentPayload))
      setDocuments((current) => [...current, ...payloads])
      event.target.value = ""
    } catch (error) {
      console.error(error)
      setDocsError("Não foi possível processar os documentos selecionados.")
    } finally {
      setIsPreparingDocs(false)
    }
  }

  const removeDocument = (index: number) => {
    setDocuments((current) => current.filter((_, i) => i !== index))
  }

  const clearDocuments = () => {
    setDocuments([])
  }

  const handleOrder = async (serviceId: string) => {
    if (isPreparingDocs) {
      alert("Aguarde o processamento dos documentos.")
      return
    }

    if (documents.length === 0) {
      alert("Adicione pelo menos um documento antes de solicitar.")
      return
    }

    setIsSubmitting(true)
    setPaymentReference(null)
    setReceipt(null)

    try {
      const order = await createOrder(serviceId)

      await attachDocuments(order.id, { documents })
      await submitOrder(order.id)

      const payment = await generatePayment(order.id)
      setPaymentReference(payment.reference)

      await confirmPayment(payment.reference)

      const receiptData = await getReceipt(order.id)
      setReceipt(receiptData)

      alert(
        `Referencia de pagamento: ${payment.reference}\nRecibo: ${receiptData.receipt_number}`
      )
    } catch (error) {
      console.error(error)
      alert("Ocorreu um erro ao processar o pedido.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div style={{ maxWidth: "960px", margin: "0 auto", padding: "32px 16px" }}>
      <header style={{ marginBottom: "24px" }}>
        <h1 style={{ marginBottom: "8px" }}>Serviços</h1>
        <p style={{ margin: 0 }}>
          Selecione o serviço, envie os documentos e finalize o pedido.
        </p>
      </header>

      <section
        style={{
          padding: "16px",
          border: "1px solid #e1e5ea",
          borderRadius: "12px",
          marginBottom: "24px"
        }}
      >
        <h2 style={{ marginTop: 0 }}>Documentos</h2>
        <p style={{ marginTop: 0, color: "#5b6673" }}>
          Envie documentos em PDF ou imagem. Vamos gerar a URI automaticamente.
        </p>

        <input
          type="file"
          multiple
          onChange={handleFileSelection}
          disabled={isPreparingDocs || isSubmitting}
        />
        {isPreparingDocs && <p>Processando documentos...</p>}
        {docsError && <p style={{ color: "#b42318" }}>{docsError}</p>}

        {documents.length > 0 && (
          <div style={{ marginTop: "16px" }}>
            <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
              {documents.map((doc, index) => (
                <div
                  key={`${doc.filename}-${index}`}
                  style={{
                    border: "1px solid #edf0f4",
                    borderRadius: "10px",
                    padding: "12px",
                    minWidth: "240px"
                  }}
                >
                  <strong>{doc.filename}</strong>
                  <p style={{ margin: "6px 0", color: "#5b6673" }}>
                    {doc.content_type} · {Math.ceil(doc.size_bytes / 1024)} KB
                  </p>
                  <button type="button" onClick={() => removeDocument(index)}>
                    Remover
                  </button>
                </div>
              ))}
            </div>
            <button
              type="button"
              onClick={clearDocuments}
              style={{ marginTop: "12px" }}
            >
              Limpar documentos
            </button>
          </div>
        )}
      </section>

      {services.map((service) => (
        <section
          key={service.id}
          style={{
            border: "1px solid #e1e5ea",
            borderRadius: "12px",
            padding: "16px",
            marginBottom: "16px"
          }}
        >
          <h3 style={{ marginTop: 0 }}>{service.name}</h3>
          <p style={{ margin: "8px 0", color: "#5b6673" }}>
            {service.price} Kz
          </p>

          <button
            onClick={() => handleOrder(service.id)}
            disabled={isSubmitting || isPreparingDocs}
          >
            {isSubmitting ? "Processando..." : "Solicitar"}
          </button>
        </section>
      ))}

      {paymentReference && (
        <section
          style={{
            border: "1px solid #e1e5ea",
            borderRadius: "12px",
            padding: "16px",
            marginTop: "24px"
          }}
        >
          <h2 style={{ marginTop: 0 }}>Pagamento</h2>
          <p>Referência: {paymentReference}</p>
        </section>
      )}

      {receipt && (
        <section
          style={{
            border: "1px solid #e1e5ea",
            borderRadius: "12px",
            padding: "16px",
            marginTop: "16px"
          }}
        >
          <h2 style={{ marginTop: 0 }}>Recibo</h2>
          <p>Número: {receipt.receipt_number}</p>
          <p>Serviço: {receipt.service_id}</p>
          <p>Valor: {receipt.amount} Kz</p>
          <p>Status: {receipt.status}</p>
        </section>
      )}
    </div>
  )
}
