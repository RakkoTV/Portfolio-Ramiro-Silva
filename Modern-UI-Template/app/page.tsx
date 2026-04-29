import Image from "next/image"
import Link from "next/link"
import { ArrowRight, Check, ChevronDown, MapPin, Phone, Users } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Card, CardContent } from "@/components/ui/card"

// URL del formulario de Google (reemplazar con la URL real)
const FORM_URL = "https://forms.google.com/your-form-url"
// Email de contacto (reemplazar con el email real)
const CONTACT_EMAIL = "info@carteleriapro.com"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Header/Navigation */}
      <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-xl">
            <MapPin className="h-5 w-5 text-primary" />
            <span>CarteleríaPro</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="#features" className="text-sm font-medium hover:text-primary">
              Características
            </Link>
            <Link href="#testimonials" className="text-sm font-medium hover:text-primary">
              Testimonios
            </Link>
            <Link href="#plans" className="text-sm font-medium hover:text-primary">
              Planes
            </Link>
            <Link href="#faq" className="text-sm font-medium hover:text-primary">
              FAQ
            </Link>
          </nav>
          <div>
            <Button asChild>
              <a href={`mailto:${CONTACT_EMAIL}`}>Contáctanos</a>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-2 lg:gap-12 xl:gap-16">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
                    Impulsa la Visibilidad de tu Marca en Cada Esquina
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    Carteles publicitarios premium que captan la atención y atraen clientes a tu negocio las 24 horas.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Button size="lg" className="gap-1" asChild>
                    <a href={FORM_URL} target="_blank" rel="noopener noreferrer">
                      Solicitar Info <ArrowRight className="h-4 w-4" />
                    </a>
                  </Button>
                  <Button size="lg" variant="outline">
                    Ver Portafolio
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative h-[350px] w-full md:h-[450px] lg:h-[500px]">
                  <Image
                    src="/placeholder.svg?height=500&width=500"
                    alt="Cartel en esquina mostrando publicidad de una cafetería"
                    fill
                    className="object-cover rounded-lg"
                    priority
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Problem/Solution Section */}
        <section className="bg-muted py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto flex max-w-[58rem] flex-col items-center justify-center gap-4 text-center">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                ¿Por qué Publicidad en Esquinas?
              </h2>
              <p className="max-w-[85%] text-muted-foreground md:text-xl">
                En un mundo digital, la presencia física sigue siendo importante. Los carteles en esquinas ofrecen
                visibilidad 24/7 en áreas de alto tráfico.
              </p>
            </div>
            <div className="mx-auto grid max-w-5xl gap-6 py-12 md:grid-cols-2 lg:gap-12">
              <div className="flex flex-col gap-2">
                <h3 className="text-xl font-bold">El Problema</h3>
                <ul className="grid gap-3">
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-destructive/20 p-1">
                      <ChevronDown className="h-4 w-4 text-destructive" />
                    </div>
                    <span>Los anuncios digitales son fácilmente ignorados o bloqueados</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-destructive/20 p-1">
                      <ChevronDown className="h-4 w-4 text-destructive" />
                    </div>
                    <span>Los negocios luchan por atraer tráfico peatonal local</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-destructive/20 p-1">
                      <ChevronDown className="h-4 w-4 text-destructive" />
                    </div>
                    <span>Las vallas publicitarias tradicionales son caras y limitadas</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-destructive/20 p-1">
                      <ChevronDown className="h-4 w-4 text-destructive" />
                    </div>
                    <span>Es difícil dirigirse a demografías específicas del vecindario</span>
                  </li>
                </ul>
              </div>
              <div className="flex flex-col gap-2">
                <h3 className="text-xl font-bold">Nuestra Solución</h3>
                <ul className="grid gap-3">
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-primary/20 p-1">
                      <Check className="h-4 w-4 text-primary" />
                    </div>
                    <span>Ubicación estratégica en esquinas de alto tráfico</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-primary/20 p-1">
                      <Check className="h-4 w-4 text-primary" />
                    </div>
                    <span>Visibilidad 24/7 para peatones y conductores</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-primary/20 p-1">
                      <Check className="h-4 w-4 text-primary" />
                    </div>
                    <span>Económico en comparación con vallas publicitarias tradicionales</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="rounded-full bg-primary/20 p-1">
                      <Check className="h-4 w-4 text-primary" />
                    </div>
                    <span>Segmentación precisa por vecindario para negocios locales</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Features and Benefits Section */}
        <section id="features" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto flex max-w-[58rem] flex-col items-center justify-center gap-4 text-center">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                Características Premium que Generan Resultados
              </h2>
              <p className="max-w-[85%] text-muted-foreground md:text-xl">
                Nuestros carteles de esquina están diseñados para maximizar la visibilidad y el impacto para tu negocio.
              </p>
            </div>
            <div className="mx-auto grid max-w-5xl gap-8 py-12 md:grid-cols-3">
              <Card>
                <CardContent className="pt-6">
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                    <MapPin className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold">Ubicación Estratégica</h3>
                  <p className="text-muted-foreground">
                    Analizamos patrones de tráfico peatonal y vehicular para colocar tus carteles en las esquinas más
                    efectivas.
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6">
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                    <Users className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold">Segmentación Demográfica</h3>
                  <p className="text-muted-foreground">
                    Dirige tu publicidad a vecindarios y demografías específicas basadas en el perfil de tu cliente
                    ideal.
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6">
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                    <Phone className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold">Integración de Código QR</h3>
                  <p className="text-muted-foreground">
                    Conecta lo offline con lo online mediante códigos QR escaneables que rastrean el engagement y las
                    conversiones.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section id="testimonials" className="bg-muted py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto flex max-w-[58rem] flex-col items-center justify-center gap-4 text-center">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                Confianza de Negocios Locales
              </h2>
              <p className="max-w-[85%] text-muted-foreground md:text-xl">
                Mira lo que dicen nuestros clientes sobre el impacto de nuestras soluciones publicitarias en esquinas.
              </p>
            </div>
            <div className="mx-auto grid max-w-5xl gap-6 py-12 md:grid-cols-2 lg:gap-12">
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-start gap-4">
                    <Image
                      src="/placeholder.svg?height=60&width=60"
                      alt="Retrato del cliente"
                      width={60}
                      height={60}
                      className="rounded-full"
                    />
                    <div>
                      <h3 className="text-lg font-bold">María Rodríguez</h3>
                      <p className="text-sm text-muted-foreground">Propietaria, Café Bueno</p>
                    </div>
                  </div>
                  <blockquote className="mt-4 border-l-2 pl-4">
                    "Desde que colocamos nuestros carteles en dos esquinas cercanas, hemos visto un aumento del 30% en
                    el tráfico peatonal. Los nuevos clientes mencionan ver nuestros carteles a diario."
                  </blockquote>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-start gap-4">
                    <Image
                      src="/placeholder.svg?height=60&width=60"
                      alt="Retrato del cliente"
                      width={60}
                      height={60}
                      className="rounded-full"
                    />
                    <div>
                      <h3 className="text-lg font-bold">David Chen</h3>
                      <p className="text-sm text-muted-foreground">Director de Marketing, Urban Fitness</p>
                    </div>
                  </div>
                  <blockquote className="mt-4 border-l-2 pl-4">
                    "El ROI de estos carteles de esquina ha sido increíble. Hemos rastreado más de 200 nuevas membresías
                    de gimnasio directamente de personas que vieron nuestra señalización en el vecindario."
                  </blockquote>
                </CardContent>
              </Card>
            </div>
            <div className="mx-auto flex max-w-[58rem] flex-wrap items-center justify-center gap-4">
              <div className="flex h-16 w-32 items-center justify-center grayscale transition-all hover:grayscale-0">
                <Image src="/placeholder.svg?height=64&width=128" alt="Logo de cliente" width={128} height={64} />
              </div>
              <div className="flex h-16 w-32 items-center justify-center grayscale transition-all hover:grayscale-0">
                <Image src="/placeholder.svg?height=64&width=128" alt="Logo de cliente" width={128} height={64} />
              </div>
              <div className="flex h-16 w-32 items-center justify-center grayscale transition-all hover:grayscale-0">
                <Image src="/placeholder.svg?height=64&width=128" alt="Logo de cliente" width={128} height={64} />
              </div>
              <div className="flex h-16 w-32 items-center justify-center grayscale transition-all hover:grayscale-0">
                <Image src="/placeholder.svg?height=64&width=128" alt="Logo de cliente" width={128} height={64} />
              </div>
            </div>
          </div>
        </section>

        {/* Plans Section (Previously Pricing) */}
        <section id="plans" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto flex max-w-[58rem] flex-col items-center justify-center gap-4 text-center">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                Nuestros Planes de Servicio
              </h2>
              <p className="max-w-[85%] text-muted-foreground md:text-xl">
                Elige el plan que mejor se adapte a las necesidades de tu negocio.
              </p>
            </div>
            <div className="mx-auto grid max-w-5xl gap-6 py-12 md:grid-cols-3">
              <Card className="flex flex-col">
                <CardContent className="pt-6">
                  <div className="mb-4 flex flex-col gap-1">
                    <h3 className="text-2xl font-bold">Inicial</h3>
                    <p className="text-muted-foreground">Perfecto para pequeños negocios locales</p>
                  </div>
                  <ul className="grid gap-3">
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>1 Cartel de esquina</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Actualización mensual de diseño</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Análisis básico de tráfico peatonal</span>
                    </li>
                  </ul>
                  <Button className="mt-6 w-full" asChild>
                    <a href={FORM_URL} target="_blank" rel="noopener noreferrer">
                      Solicitar Información
                    </a>
                  </Button>
                </CardContent>
              </Card>
              <Card className="flex flex-col border-primary">
                <CardContent className="pt-6">
                  <div className="mb-4 flex flex-col gap-1">
                    <h3 className="text-2xl font-bold">Crecimiento</h3>
                    <p className="text-muted-foreground">El más popular para negocios en crecimiento</p>
                  </div>
                  <ul className="grid gap-3">
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>3 Carteles de esquina</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Actualización quincenal de diseño</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Análisis avanzado de tráfico</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Integración de código QR</span>
                    </li>
                  </ul>
                  <Button className="mt-6 w-full" asChild>
                    <a href={FORM_URL} target="_blank" rel="noopener noreferrer">
                      Solicitar Información
                    </a>
                  </Button>
                </CardContent>
              </Card>
              <Card className="flex flex-col">
                <CardContent className="pt-6">
                  <div className="mb-4 flex flex-col gap-1">
                    <h3 className="text-2xl font-bold">Premium</h3>
                    <p className="text-muted-foreground">Para negocios establecidos</p>
                  </div>
                  <ul className="grid gap-3">
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>7 Carteles de esquina</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Actualización semanal de diseño</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Panel de análisis premium</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Código QR con seguimiento de conversiones</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span>Gestor de cuenta dedicado</span>
                    </li>
                  </ul>
                  <Button className="mt-6 w-full" asChild>
                    <a href={FORM_URL} target="_blank" rel="noopener noreferrer">
                      Solicitar Información
                    </a>
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section id="faq" className="bg-muted py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto flex max-w-[58rem] flex-col items-center justify-center gap-4 text-center">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Preguntas Frecuentes</h2>
              <p className="max-w-[85%] text-muted-foreground md:text-xl">
                Encuentra respuestas a preguntas comunes sobre nuestras soluciones publicitarias en esquinas.
              </p>
            </div>
            <div className="mx-auto max-w-3xl py-12">
              <Accordion type="single" collapsible className="w-full">
                <AccordionItem value="item-1">
                  <AccordionTrigger>¿Cuánto tiempo tarda la instalación de mis carteles?</AccordionTrigger>
                  <AccordionContent>
                    Una vez que tu diseño es aprobado, normalmente instalamos los carteles en 7-10 días hábiles. Para
                    necesidades urgentes, ofrecemos instalación acelerada.
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-2">
                  <AccordionTrigger>¿Necesito permisos para carteles en esquinas?</AccordionTrigger>
                  <AccordionContent>
                    Sí, se requieren permisos para publicidad en esquinas. Nuestro servicio incluye la gestión de todos
                    los permisos y requisitos legales necesarios, para que no tengas que preocuparte por el papeleo.
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-3">
                  <AccordionTrigger>¿Cómo determinan las mejores ubicaciones para mis carteles?</AccordionTrigger>
                  <AccordionContent>
                    Utilizamos una combinación de datos de tráfico peatonal, patrones de tráfico vehicular e información
                    demográfica para identificar las esquinas óptimas para tu público objetivo. Te proporcionaremos
                    recomendaciones basadas en los objetivos de tu negocio y el perfil de tu cliente ideal.
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-4">
                  <AccordionTrigger>¿Qué sucede si mi cartel es dañado o vandalizado?</AccordionTrigger>
                  <AccordionContent>
                    Todos nuestros planes incluyen mantenimiento y protección contra daños. Si tu cartel es dañado o
                    vandalizado, lo repararemos o reemplazaremos sin costo adicional dentro de las 48 horas posteriores
                    a la notificación.
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-5">
                  <AccordionTrigger>¿Puedo cambiar mi diseño durante el período del contrato?</AccordionTrigger>
                  <AccordionContent>
                    ¡Sí! Cada plan incluye actualizaciones regulares de diseño. La frecuencia depende del nivel de tu
                    plan. Se pueden adquirir cambios de diseño adicionales por separado si es necesario.
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>
          </div>
        </section>

        {/* Final CTA Section */}
        <section id="contact" className="py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto grid max-w-5xl gap-6 lg:grid-cols-2">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
                    ¿Listo para Impulsar tu Visibilidad Local?
                  </h2>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    Comienza hoy y descubre cómo la publicidad en esquinas puede transformar la presencia de tu negocio.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Button size="lg" className="gap-1" asChild>
                    <a href={FORM_URL} target="_blank" rel="noopener noreferrer">
                      Quiero Información <ArrowRight className="h-4 w-4" />
                    </a>
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative h-[300px] w-full md:h-[400px]">
                  <Image
                    src="/placeholder.svg?height=400&width=600"
                    alt="Cartel de esquina en una intersección urbana concurrida"
                    fill
                    className="object-cover rounded-lg"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t bg-background">
        <div className="container flex flex-col gap-6 py-8 md:flex-row md:items-center md:justify-between md:py-12">
          <div className="flex items-center gap-2 font-bold text-xl">
            <MapPin className="h-5 w-5 text-primary" />
            <span>CarteleríaPro</span>
          </div>
          <nav className="flex flex-wrap gap-4 md:gap-6">
            <Link href="#" className="text-sm font-medium hover:text-primary">
              Términos
            </Link>
            <Link href="#" className="text-sm font-medium hover:text-primary">
              Privacidad
            </Link>
            <a href={`mailto:${CONTACT_EMAIL}`} className="text-sm font-medium hover:text-primary">
              Contacto
            </a>
          </nav>
          <p className="text-sm text-muted-foreground">© 2023 CarteleríaPro. Todos los derechos reservados.</p>
        </div>
      </footer>
    </div>
  )
}

