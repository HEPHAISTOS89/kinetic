import SwiftUI

struct HomeView: View {
    var body: some View {
        ZStack {
            LinearGradient(colors: [.purple, .indigo, .pink], startPoint: .top, endPoint: .bottom)
            VStack(spacing: 13) {
                Text("Hey Sam 👋").font(.system(size: 31, weight: .bold))
                Text("Supercharge your day").font(.system(size: 15)).multilineTextAlignment(.center)
                    .minimumScaleFactor(0.5)
                Button(action: {}) {
                    Image(systemName: "line.3.horizontal")
                }
                .frame(width: 28, height: 28)
                Button { } label: { Image(systemName: "heart") }
                VStack { Text("Card") }.padding(17).background(.ultraThinMaterial).cornerRadius(18).shadow(radius: 20)
                VStack { Text("Card 2") }.padding(10).background(.ultraThinMaterial).cornerRadius(11)
                Text("Card 3").font(.custom("Poppins", fixedSize: 14))
                Rectangle().frame(width: 390, height: 844)
            }
            .animation(.bouncy, value: true)
            .dynamicTypeSize(.large)
        }
    }
}
