// Signature stubs of the Jetpack Compose APIs used by `kinetic export --stack compose`.
// They let kotlinc check syntax and typing of the generated file without the
// Compose artifacts. They are NOT the real API: a pass here is not a Gradle build.
@file:Suppress("unused", "UNUSED_PARAMETER")
package androidx.compose.runtime
@Target(AnnotationTarget.FUNCTION, AnnotationTarget.TYPE, AnnotationTarget.TYPE_PARAMETER, AnnotationTarget.PROPERTY_GETTER)
annotation class Composable
annotation class Immutable
class ProvidedValue<T>
class ProvidableCompositionLocal<T> { infix fun provides(value: T): ProvidedValue<T> = ProvidedValue() }
fun <T> staticCompositionLocalOf(defaultFactory: () -> T): ProvidableCompositionLocal<T> = ProvidableCompositionLocal()
fun CompositionLocalProvider(vararg values: ProvidedValue<*>, content: () -> Unit) = content()
