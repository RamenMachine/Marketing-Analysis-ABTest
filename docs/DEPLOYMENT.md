# Deployment Guide

This guide covers deploying the Marketing A/B Test Evaluation Platform to various hosting services.

## Prerequisites

- Build the project: `npm run build`
- Ensure all dependencies are installed
- Have a GitHub account (for most deployment options)

## Deployment Options

### 1. Vercel (Recommended)

**Steps:**
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Configure build settings:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Click "Deploy"

**Advantages:**
- Automatic deployments on git push
- Free tier available
- Fast CDN
- Custom domains

### 2. Netlify

**Steps:**
1. Push your code to GitHub
2. Go to [netlify.com](https://netlify.com)
3. Click "New site from Git"
4. Connect your GitHub repository
5. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
6. Click "Deploy site"

**Advantages:**
- Easy setup
- Free tier available
- Form handling (if needed later)
- Branch previews

### 3. GitHub Pages

**Steps:**
1. Install gh-pages: `npm install -g gh-pages`
2. Add to `package.json`:
   ```json
   "scripts": {
     "deploy": "npm run build && gh-pages -d dist"
   }
   ```
3. Run: `npm run deploy`
4. Enable GitHub Pages in repository settings
5. Select `gh-pages` branch as source

**Advantages:**
- Free hosting
- Integrated with GitHub
- Custom domain support

### 4. AWS S3 + CloudFront

**Steps:**
1. Build the project: `npm run build`
2. Create an S3 bucket
3. Upload `dist/` contents to S3
4. Enable static website hosting
5. Create CloudFront distribution
6. Point to S3 bucket

**Advantages:**
- Scalable
- Professional setup
- Custom domain with SSL

## Environment Variables

If you need environment variables:

1. Create `.env.production` file
2. Add variables:
   ```
   VITE_API_URL=https://api.example.com
   ```
3. Access in code: `import.meta.env.VITE_API_URL`

## Post-Deployment Checklist

- [ ] Test all dashboard features
- [ ] Verify JSON data loading
- [ ] Check responsive design on mobile
- [ ] Test export functionality
- [ ] Verify all links work
- [ ] Check console for errors
- [ ] Test with different browsers

## Custom Domain

### Vercel/Netlify:
1. Go to project settings
2. Add custom domain
3. Follow DNS configuration instructions

### GitHub Pages:
1. Add `CNAME` file to repository
2. Configure DNS records
3. Wait for propagation

## Troubleshooting

### Build Fails
- Check Node.js version (16+ required)
- Clear `node_modules` and reinstall
- Check for TypeScript errors

### Assets Not Loading
- Verify `base` path in `vite.config.js`
- Check public folder structure
- Ensure JSON files are in `public/` directory

### Routing Issues
- Configure redirect rules for SPA
- Use hash routing if needed
- Check base URL configuration

## Performance Optimization

1. **Enable Compression**: Gzip/Brotli compression
2. **CDN**: Use CloudFront or similar
3. **Caching**: Set appropriate cache headers
4. **Code Splitting**: Already handled by Vite
5. **Image Optimization**: Optimize any images

## Monitoring

Consider adding:
- Google Analytics
- Error tracking (Sentry)
- Performance monitoring
- User analytics

---

For questions or issues, please open a GitHub issue.

