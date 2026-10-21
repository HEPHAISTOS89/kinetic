@file:Suppress("unused", "UNUSED_PARAMETER")
package androidx.compose.animation.core
object Spring
class SpringSpec<T>(val dampingRatio: Float, val stiffness: Float)
fun <T> spring(dampingRatio: Float = 1f, stiffness: Float = 1500f, visibilityThreshold: T? = null): SpringSpec<T> =
    SpringSpec(dampingRatio, stiffness)
