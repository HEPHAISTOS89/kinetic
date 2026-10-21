// Kinetic eval harness: renders every entry of `Gallery.screens` to PNG,
// light + dark at the default text size, at iPhone 15/16 size (393×852 pt).
import SwiftUI
import AppKit

@main
struct RenderMain {
    @MainActor static func main() {
        let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "."
        try? FileManager.default.createDirectory(atPath: out, withIntermediateDirectories: true)
        for (name, view) in Gallery.screens {
            for (scheme, label) in [(ColorScheme.light, "light"), (.dark, "dark")] {
                // macOS ImageRenderer ignores Dynamic Type scaling: XXL renders need the iOS Simulator.
                for (size, sizeLabel) in [(DynamicTypeSize.large, "default")] {
                    let appearance = NSAppearance(named: scheme == .dark ? .darkAqua : .aqua)!
                    appearance.performAsCurrentDrawingAppearance {
                        let content = view
                            .fixedSize(horizontal: false, vertical: true)
                            .frame(width: 393, height: 852, alignment: .top)
                            .clipped()
                            .environment(\.colorScheme, scheme)
                            .environment(\.dynamicTypeSize, size)
                            .background(scheme == .dark ? Color.black : Color.white)
                        let r = ImageRenderer(content: content)
                        r.scale = 2
                        if let img = r.nsImage, let tiff = img.tiffRepresentation,
                           let rep = NSBitmapImageRep(data: tiff), let png = rep.representation(using: .png, properties: [:]) {
                            let file = "\(out)/\(name)-\(label)-\(sizeLabel).png"
                            try? png.write(to: URL(fileURLWithPath: file))
                            print(file)
                        }
                    }
                }
            }
        }
    }
}
