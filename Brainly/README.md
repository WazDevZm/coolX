# 🧠 TriviaMaster - Next.js Landing Page

A stunning, modern landing page for a trivia question app built with Next.js 14, TypeScript, Tailwind CSS, and Framer Motion.

## ✨ Features

- **Modern Design**: Clean, professional UI with smooth animations
- **Responsive**: Fully responsive design that works on all devices
- **Interactive**: Engaging animations and hover effects
- **Performance**: Optimized for speed and SEO
- **Accessibility**: Built with accessibility best practices

## 🚀 Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety and better development experience
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations and transitions
- **Lucide React** - Beautiful, customizable icons

## 🎨 Design Features

### Color Palette
- **Primary Green**: `#22c55e` - Success, growth, knowledge
- **Orange**: `#f59e0b` - Energy, enthusiasm
- **Blue**: `#3b82f6` - Trust, intelligence
- **Purple**: `#8b5cf6` - Creativity, wisdom

### Key Sections
1. **Hero Section** - Eye-catching introduction with live question preview
2. **Statistics** - Impressive numbers and achievements
3. **Features** - Key app capabilities with icons
4. **Categories** - Interactive category cards
5. **Call-to-Action** - Compelling signup section
6. **Footer** - Complete site navigation

## 🛠️ Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Brainly
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📱 Responsive Design

The landing page is fully responsive and optimized for:
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: 1024px+

## 🎭 Animations

Built with Framer Motion for smooth, professional animations:
- **Page Load**: Staggered element animations
- **Scroll Triggers**: Elements animate into view
- **Hover Effects**: Interactive button and card animations
- **Live Elements**: Rotating questions and floating icons

## 🎯 Key Components

### Hero Section
- Animated logo and navigation
- Live question preview with countdown
- Call-to-action buttons
- Floating trophy and star elements

### Interactive Features
- **Live Question Rotator**: Cycles through sample questions
- **Animated Statistics**: Number counters and progress bars
- **Hover Effects**: Cards lift and transform on hover
- **Smooth Scrolling**: Navigation links with smooth scroll

### Performance Optimizations
- **Image Optimization**: Next.js automatic image optimization
- **Code Splitting**: Automatic code splitting for faster loads
- **SEO Ready**: Meta tags and structured data
- **Accessibility**: ARIA labels and keyboard navigation

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to customize the color palette:

```javascript
colors: {
  trivia: {
    green: '#22c55e',
    orange: '#f59e0b', 
    blue: '#3b82f6',
    purple: '#8b5cf6',
  }
}
```

### Content
Update the content in `app/page.tsx`:
- Hero text and CTAs
- Feature descriptions
- Category information
- Statistics and numbers

## 📦 Build & Deploy

### Build for Production
```bash
npm run build
```

### Start Production Server
```bash
npm start
```

### Deploy to Vercel
```bash
npx vercel
```

## 🔧 Development

### File Structure
```
Brainly/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
├── public/
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

### Adding New Sections
1. Create new components in `components/`
2. Import and use in `app/page.tsx`
3. Add responsive classes and animations
4. Test across all device sizes

## 🎯 Future Enhancements

- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] User authentication
- [ ] Real-time leaderboards
- [ ] Social sharing features
- [ ] Progressive Web App (PWA)

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using Next.js, TypeScript, and Tailwind CSS**
