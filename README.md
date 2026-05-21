<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexaura — Personal AI Operating System</title>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700;800&family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <style>
        /* ─── CSS VARIABLES & THEME ─── */
        :root {
            --bg: #030712;
            --bg2: #080f1f;
            --bg3: #0d1628;
            --surface: #111827;
            --surface2: #1a2236;
            --border: rgba(255, 255, 255, 0.08);
            --border-bright: rgba(99, 179, 237, 0.3);
            --accent: #38bdf8;
            --accent-hover: #0ea5e9;
            --accent2: #818cf8;
            --accent3: #34d399;
            --accent4: #fb923c;
            --glow: rgba(56, 189, 248, 0.15);
            --glow2: rgba(129, 140, 248, 0.1);
            --text: #f8fafc;
            --muted: rgba(148, 163, 184, 0.8);
            --muted2: #94a3b8;
            --mono: 'JetBrains Mono', monospace;
            --sans: 'Outfit', sans-serif;
            --radius: 12px;
            --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* ─── RESET & BASE STYLES ─── */
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: var(--sans);
            overflow-x: hidden;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* ─── BACKGROUND EFFECTS ─── */
        body::after {
            content: '';
            position: fixed;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: 9999;
            opacity: 0.5;
        }

        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image: 
                linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none;
            z-index: 0;
        }

        /* ─── NAVIGATION ─── */
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 500;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 48px;
            background: rgba(3, 7, 18, 0.75);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid var(--border);
        }

        .nav-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: var(--mono);
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: 0.2em;
            text-transform: uppercase;
        }

        .nav-logo-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 12px var(--accent);
            animation: pulse-dot 2.5s ease-in-out infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.8); }
        }

        .nav-links {
            display: flex;
            gap: 36px;
            list-style: none;
            align-items: center;
        }

        .nav-links a {
            font-family: var(--mono);
            font-size: 0.65rem;
            letter-spacing: 0.15em;
            color: var(--muted2);
            text-decoration: none;
            text-transform: uppercase;
            transition: var(--transition-smooth);
        }

        .nav-links a:hover {
            color: var(--accent);
            text-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
        }

        .nav-cta {
            font-family: var(--mono);
            font-size: 0.65rem;
            letter-spacing: 0.1em;
            color: var(--accent);
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 8px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 700;
            transition: var(--transition-smooth);
            text-transform: uppercase;
        }

        .nav-cta:hover {
            background: rgba(56, 189, 248, 0.15);
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
        }

        /* ─── HERO SECTION ─── */
        .hero {
            position: relative;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 120px 24px 60px;
            z-index: 1;
            overflow: hidden;
        }

        /* Ambient glowing orbs */
        .haze {
            position: absolute;
            border-radius: 50%;
            filter: blur(140px);
            pointer-events: none;
            animation: haze-drift 15s ease-in-out infinite alternate;
        }

        .haze-1 {
            width: 700px;
            height: 700px;
            background: radial-gradient(ellipse, rgba(56, 189, 248, 0.1), transparent 70%);
            top: -10%;
            left: -15%;
            animation-delay: 0s;
        }

        .haze-2 {
            width: 600px;
            height: 600px;
            background: radial-gradient(ellipse, rgba(129, 140, 248, 0.08), transparent 70%);
            top: 15%;
            right: -10%;
            animation-delay: -5s;
        }

        .haze-3 {
            width: 500px;
            height: 500px;
            background: radial-gradient(ellipse, rgba(52, 211, 153, 0.06), transparent 70%);
            bottom: 5%;
            left: 25%;
            animation-delay: -10s;
        }

        @keyframes haze-drift {
            from { transform: translate(0, 0) scale(1); }
            to { transform: translate(60px, 40px) scale(1.1); }
        }

        #particles-canvas {
            position: absolute;
            inset: 0;
            pointer-events: none;
            z-index: 0;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-family: var(--mono);
            font-size: 0.65rem;
            letter-spacing: 0.15em;
            color: var(--accent3);
            background: rgba(52, 211, 153, 0.08);
            border: 1px solid rgba(52, 211, 153, 0.25);
            padding: 8px 18px;
            border-radius: 100px;
            margin-bottom: 32px;
            text-transform: uppercase;
            box-shadow: 0 0 20px rgba(52, 211, 153, 0.1);
        }

        .hero-badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--accent3);
            animation: pulse-dot 1.5s ease-in-out infinite;
        }

        .hero h1 {
            font-family: var(--mono);
            font-size: clamp(3.5rem, 10vw, 8.5rem);
            font-weight: 800;
            letter-spacing: 0.05em;
            line-height: 1.1;
            margin-bottom: 8px;
            position: relative;
            background: linear-gradient(135deg, #ffffff 0%, #bae6fd 25%, #38bdf8 50%, #818cf8 75%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0px 4px 20px rgba(56, 189, 248, 0.2));
        }

        .hero-sub-line {
            font-family: var(--mono);
            font-size: 0.75rem;
            letter-spacing: 0.35em;
            color: var(--muted);
            text-transform: uppercase;
            margin-bottom: 32px;
        }

        .hero-desc {
            max-width: 640px;
            font-size: 1.15rem;
            color: var(--muted2);
            line-height: 1.8;
            margin-bottom: 48px;
            font-weight: 300;
        }

        .hero-desc strong {
            color: var(--text);
            font-weight: 600;
        }

        .hero-btns {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: 70px;
        }

        .btn-glow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 32px;
            background: var(--accent);
            color: #020817;
            border: none;
            border-radius: 8px;
            font-family: var(--mono);
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-weight: 800;
            text-decoration: none;
            cursor: pointer;
            transition: var(--transition-smooth);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4), 0 0 40px rgba(56, 189, 248, 0.1);
        }

        .btn-glow:hover {
            transform: translateY(-3px);
            background: var(--accent-hover);
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.6), 0 0 60px rgba(56, 189, 248, 0.3);
        }

        .btn-ghost {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 32px;
            background: rgba(255, 255, 255, 0.02);
            color: var(--text);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            font-family: var(--mono);
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: var(--transition-smooth);
            backdrop-filter: blur(12px);
        }

        .btn-ghost:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(56, 189, 248, 0.05);
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        /* ─── STATS BAR ─── */
        .stats-bar {
            display: flex;
            gap: 0;
            border: 1px solid var(--border-bright);
            border-radius: var(--radius);
            overflow: hidden;
            background: rgba(8, 15, 31, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            max-width: 720px;
            width: 100%;
            margin: 0 auto 60px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .stat-item {
            flex: 1;
            padding: 20px 24px;
            text-align: center;
            border-right: 1px solid var(--border-bright);
            position: relative;
            transition: var(--transition-smooth);
        }
        
        .stat-item:hover {
            background: rgba(56, 189, 248, 0.05);
        }

        .stat-item:last-child {
            border-right: none;
        }

        .stat-num {
            font-family: var(--mono);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
            letter-spacing: -0.02em;
        }

        .stat-num span {
            color: var(--accent);
        }

        .stat-label {
            font-family: var(--mono);
            font-size: 0.55rem;
            letter-spacing: 0.15em;
            color: var(--muted);
            text-transform: uppercase;
            margin-top: 4px;
        }

        /* ─── TERMINAL COMPONENT ─── */
        .terminal-wrap {
            width: 100%;
            max-width: 760px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .terminal-glow-ring {
            position: absolute;
            inset: -2px;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(56,189,248,0.4), rgba(129,140,248,0.4), rgba(52,211,153,0.2));
            padding: 1px;
            z-index: -1;
            filter: blur(4px);
        }

        .terminal {
            background: rgba(8, 15, 31, 0.85);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        .t-bar {
            background: rgba(3, 7, 18, 0.95);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 14px 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .t-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        .t-red { background: #ff5f57; box-shadow: 0 0 10px rgba(255,95,87,0.4); }
        .t-yellow { background: #febc2e; box-shadow: 0 0 10px rgba(254,188,46,0.4); }
        .t-green { background: #28c840; box-shadow: 0 0 10px rgba(40,200,64,0.4); }

        .t-title {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: rgba(148, 163, 184, 0.6);
            letter-spacing: 0.08em;
            margin: 0 auto;
            user-select: none;
        }

        .t-tabs {
            display: flex;
            gap: 4px;
            margin-left: auto;
        }

        .t-tab {
            font-family: var(--mono);
            font-size: 0.55rem;
            letter-spacing: 0.08em;
            color: var(--muted);
            background: rgba(255, 255, 255, 0.03);
            padding: 4px 12px;
            border-radius: 4px;
            border: 1px solid transparent;
            cursor: pointer;
            transition: var(--transition-smooth);
        }

        .t-tab:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .t-tab.active {
            color: var(--accent);
            background: rgba(56, 189, 248, 0.1);
            border-color: rgba(56, 189, 248, 0.3);
        }

        .t-body {
            padding: 24px 28px;
            font-family: var(--mono);
            font-size: 0.75rem;
            line-height: 2;
            text-align: left;
            min-height: 260px;
        }

        .t-line {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 2px 0;
        }

        .t-prompt { color: rgba(56, 189, 248, 0.8); flex-shrink: 0; user-select: none; }
        .t-cmd { color: #e2e8f0; font-weight: 500; }
        .t-ok { color: #4ade80; }
        .t-err { color: #f87171; }
        .t-sys { color: #60a5fa; }
        .t-warn { color: #fbbf24; }
        .t-dim { color: rgba(148, 163, 184, 0.5); }
        .t-highlight { color: var(--accent); }
        
        .t-cursor {
            display: inline-block;
            width: 8px;
            height: 15px;
            background: var(--accent);
            animation: blink 1s steps(1) infinite;
            vertical-align: middle;
            margin-left: 4px;
            border-radius: 1px;
            box-shadow: 0 0 8px var(--accent);
        }

        @keyframes blink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
        }

        .t-progress {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .t-bar-mini {
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            flex: 1;
            overflow: hidden;
        }

        .t-bar-fill {
            height: 100%;
            border-radius: 4px;
            animation: fill-bar 1.5s ease-out forwards;
        }

        .t-bar-fill.b1 { background: var(--accent3); animation-delay: 0.3s; width: 0; box-shadow: 0 0 10px var(--accent3); }
        .t-bar-fill.b2 { background: var(--accent); animation-delay: 0.6s; width: 0; box-shadow: 0 0 10px var(--accent); }

        @keyframes fill-bar {
            to { width: 100%; }
        }

        /* ─── GENERAL SECTIONS ─── */
        section {
            position: relative;
            z-index: 1;
        }

        .section-inner {
            max-width: 1120px;
            margin: 0 auto;
            padding: 120px 32px;
        }

        .section-eyebrow {
            font-family: var(--mono);
            font-size: 0.65rem;
            letter-spacing: 0.25em;
            color: var(--accent);
            text-transform: uppercase;
            margin-bottom: 12px;
            font-weight: 700;
        }

        .section-title {
            font-size: clamp(2.2rem, 5vw, 3.5rem);
            font-weight: 800;
            color: var(--text);
            margin-bottom: 16px;
            line-height: 1.15;
            letter-spacing: -0.02em;
        }

        .section-sub {
            font-size: 1.1rem;
            color: var(--muted2);
            max-width: 600px;
            line-height: 1.75;
            font-weight: 300;
        }

        /* ─── DATA STREAM DECORATION ─── */
        .stream-line {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 1px;
            background: linear-gradient(to bottom, transparent, rgba(56, 189, 248, 0.3), transparent);
            pointer-events: none;
            animation: stream-fall 5s linear infinite;
        }

        .stream-line:nth-child(2) { left: 15%; animation-delay: -1.5s; opacity: 0.6; }
        .stream-line:nth-child(3) { left: 65%; animation-delay: -3.2s; opacity: 0.4; }
        .stream-line:nth-child(4) { left: 85%; animation-delay: -0.8s; opacity: 0.5; }

        @keyframes stream-fall {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }

        /* ─── ARCHITECTURE FLOW PIPELINE ─── */
        .arch-container {
            margin-top: 64px;
            position: relative;
        }

        .arch-bg {
            background: var(--bg2);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 56px 48px;
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 0 80px rgba(0,0,0,0.5);
        }

        .arch-bg::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(ellipse at 50% 0%, rgba(56, 189, 248, 0.08), transparent 70%);
            pointer-events: none;
        }

        .flow-pipeline {
            display: flex;
            align-items: stretch;
            gap: 12px;
            position: relative;
            z-index: 2;
        }

        .flow-node {
            flex: 1;
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: var(--radius);
            padding: 28px 24px;
            cursor: pointer;
            transition: var(--transition-smooth);
            position: relative;
            overflow: hidden;
        }

        .flow-node:hover {
            border-color: rgba(56, 189, 248, 0.5);
            background: rgba(30, 42, 60, 0.95);
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(56, 189, 248, 0.15);
        }

        .flow-node::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--node-color, var(--accent));
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .flow-node:hover::before {
            transform: scaleX(1);
        }

        .flow-arrow {
            display: flex;
            align-items: center;
            padding: 0 8px;
            flex-shrink: 0;
            color: rgba(56, 189, 248, 0.4);
            font-size: 1.2rem;
            font-family: var(--mono);
        }

        .fn-tag {
            font-family: var(--mono);
            font-size: 0.6rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            padding: 4px 10px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 14px;
            font-weight: 800;
        }

        .fn-amber { background: rgba(251, 191, 36, 0.15); color: #fcd34d; border: 1px solid rgba(251, 191, 36, 0.2); --node-color: #fcd34d; }
        .fn-blue  { background: rgba(56, 189, 248, 0.15); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.2); --node-color: #7dd3fc; }
        .fn-green { background: rgba(52, 211, 153, 0.15); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.2); --node-color: #6ee7b7; }
        .fn-purple{ background: rgba(167, 139, 250, 0.15); color: #c4b5fd; border: 1px solid rgba(167, 139, 250, 0.2); --node-color: #c4b5fd; }

        .fn-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 8px;
        }

        .fn-meta {
            font-family: var(--mono);
            font-size: 0.6rem;
            letter-spacing: 0.1em;
            color: var(--muted);
            margin-bottom: 12px;
            text-transform: uppercase;
        }

        .fn-desc {
            font-size: 0.85rem;
            color: var(--muted2);
            line-height: 1.6;
        }

        .fn-more {
            font-family: var(--mono);
            font-size: 0.6rem;
            color: var(--accent);
            opacity: 0;
            transition: opacity 0.3s;
            margin-top: 16px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-weight: 700;
        }

        .flow-node:hover .fn-more {
            opacity: 1;
        }

        /* ─── ARCHITECTURE DETAIL CARDS ─── */
        .arch-detail-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 24px;
        }

        .arch-detail-card {
            background: rgba(3, 7, 18, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            transition: var(--transition-smooth);
        }

        .arch-detail-card:hover {
            border-color: rgba(56, 189, 248, 0.3);
            background: rgba(3, 7, 18, 0.8);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }

        .adc-label {
            font-family: var(--mono);
            font-size: 0.55rem;
            letter-spacing: 0.12em;
            color: var(--accent);
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 700;
        }

        .adc-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 6px;
        }

        .adc-desc {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--muted2);
            line-height: 1.6;
        }

        /* ─── FEATURES GRID ─── */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 60px;
        }

        @media (max-width: 900px) { .features-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 600px) { 
            .features-grid { grid-template-columns: 1fr; } 
            .flow-pipeline { flex-direction: column; } 
            .flow-arrow { transform: rotate(90deg); padding: 12px 0; text-align: center; } 
        }

        .feat-card {
            background: var(--surface);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: var(--radius);
            padding: 28px 24px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: var(--transition-smooth);
        }

        .feat-card:hover {
            transform: translateY(-6px);
            border-color: rgba(56, 189, 248, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 40px rgba(56, 189, 248, 0.08);
            background: var(--surface2);
        }

        .feat-card::after {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(ellipse at 50% 0%, rgba(56, 189, 248, 0.06), transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
            pointer-events: none;
        }

        .feat-card:hover::after {
            opacity: 1;
        }

        .feat-top-bar {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--feat-color, var(--accent)), transparent);
            transform: scaleX(0);
            transform-origin: center;
            transition: transform 0.4s ease-out;
        }

        .feat-card:hover .feat-top-bar {
            transform: scaleX(1);
        }

        .feat-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: var(--mono);
            font-size: 0.6rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            padding: 6px 10px;
            border-radius: 6px;
            margin-bottom: 16px;
            font-weight: 800;
            border: 1px solid;
            width: fit-content;
        }

        .fb-blue   { background: rgba(56, 189, 248, 0.1); color: #7dd3fc; border-color: rgba(56, 189, 248, 0.2); }
        .fb-purple { background: rgba(167, 139, 250, 0.1); color: #c4b5fd; border-color: rgba(167, 139, 250, 0.2); }
        .fb-green  { background: rgba(52, 211, 153, 0.1); color: #6ee7b7; border-color: rgba(52, 211, 153, 0.2); }
        .fb-amber  { background: rgba(251, 191, 36, 0.1); color: #fcd34d; border-color: rgba(251, 191, 36, 0.2); }
        .fb-red    { background: rgba(248, 113, 113, 0.1); color: #fca5a5; border-color: rgba(248, 113, 113, 0.2); }
        .fb-teal   { background: rgba(45, 212, 191, 0.1); color: #5eead4; border-color: rgba(45, 212, 191, 0.2); }

        .feat-title {
            font-size: 1rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 10px;
            line-height: 1.3;
        }

        .feat-desc {
            font-family: var(--mono);
            font-size: 0.7rem;
            color: var(--muted2);
            line-height: 1.75;
            flex-grow: 1;
        }

        .feat-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 18px;
            padding-top: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        .feat-detail-btn {
            font-family: var(--mono);
            font-size: 0.6rem;
            color: var(--accent);
            opacity: 0;
            transition: opacity 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }

        .feat-card:hover .feat-detail-btn {
            opacity: 1;
        }

        .feat-status {
            font-family: var(--mono);
            font-size: 0.55rem;
            letter-spacing: 0.08em;
            color: var(--accent3);
            text-transform: uppercase;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .feat-status::before {
            content: '';
            display: inline-block;
            width: 6px;
            height: 6px;
            background: currentColor;
            border-radius: 50%;
            box-shadow: 0 0 8px currentColor;
        }

        .feat-status-inactive {
            color: rgba(148, 163, 184, 0.5);
        }
        .feat-status-inactive::before {
            box-shadow: none;
        }

        /* ─── MODAL STYLES ─── */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(3, 7, 18, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            z-index: 900;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .modal-content {
            background: var(--bg3);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 16px;
            width: 90%;
            max-width: 680px;
            max-height: 85vh;
            overflow-y: auto;
            padding: 40px;
            position: relative;
            transform: scale(0.95) translateY(20px);
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 40px 100px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255,255,255,0.05);
        }

        .modal-overlay.active .modal-content {
            transform: scale(1) translateY(0);
        }

        /* Custom Scrollbar for Modal */
        .modal-content::-webkit-scrollbar { width: 8px; }
        .modal-content::-webkit-scrollbar-track { background: transparent; }
        .modal-content::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.3); border-radius: 4px; }
        .modal-content::-webkit-scrollbar-thumb:hover { background: rgba(56, 189, 248, 0.5); }

        .modal-close {
            position: absolute;
            top: 20px;
            right: 20px;
            font-family: var(--mono);
            font-size: 0.75rem;
            color: var(--muted);
            cursor: pointer;
            transition: var(--transition-smooth);
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            padding: 6px 12px;
            border-radius: 6px;
        }

        .modal-close:hover {
            color: var(--text);
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .modal-head {
            display: flex;
            align-items: flex-start;
            gap: 16px;
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
        }

        .modal-icon-box {
            padding: 12px 16px;
            border-radius: 8px;
            font-family: var(--mono);
            font-size: 0.8rem;
            font-weight: 800;
            flex-shrink: 0;
        }

        .modal-info .modal-title {
            font-size: 1.3rem;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 6px;
        }

        .modal-info .modal-sub {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--muted);
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .modal-body {
            font-size: 0.95rem;
            color: var(--muted2);
            line-height: 1.8;
            margin-bottom: 28px;
            white-space: pre-wrap;
        }

        .modal-body strong {
            color: var(--text);
            font-weight: 600;
        }

        .modal-section-label {
            font-family: var(--mono);
            font-size: 0.65rem;
            letter-spacing: 0.15em;
            color: var(--accent);
            text-transform: uppercase;
            margin-bottom: 12px;
            font-weight: 700;
        }

        .modal-code-block {
            background: rgba(3, 7, 18, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-left: 4px solid var(--accent);
            padding: 20px;
            border-radius: 0 8px 8px 0;
            font-family: var(--mono);
            font-size: 0.75rem;
            color: var(--text);
            line-height: 1.7;
            white-space: pre;
            overflow-x: auto;
            margin-bottom: 24px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
        }

        .modal-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }

        .modal-tag {
            font-family: var(--mono);
            font-size: 0.6rem;
            letter-spacing: 0.08em;
            color: var(--muted2);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 6px 12px;
            border-radius: 6px;
            text-transform: uppercase;
        }

        /* ─── TECH STACK SECTION ─── */
        .stack-section {
            background: var(--bg2);
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
        }

        .stack-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 16px;
            margin-top: 50px;
        }

        .stack-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 24px 20px;
            cursor: pointer;
            transition: var(--transition-smooth);
            position: relative;
            overflow: hidden;
        }

        .stack-card:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-4px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(56, 189, 248, 0.05);
            background: rgba(30, 42, 60, 0.9);
        }

        .stack-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--sc-color, var(--accent)), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .stack-card:hover::before { opacity: 1; }

        .stack-cat {
            font-family: var(--mono);
            font-size: 0.55rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 8px;
            font-weight: 700;
        }

        .stack-name {
            font-size: 1rem;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 4px;
        }

        .stack-ver {
            font-family: var(--mono);
            font-size: 0.6rem;
            color: var(--muted);
            margin-bottom: 6px;
        }

        .stack-role {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--muted2);
        }

        .stack-more {
            font-family: var(--mono);
            font-size: 0.55rem;
            color: var(--accent);
            opacity: 0;
            transition: opacity 0.3s;
            margin-top: 12px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
        }

        .stack-card:hover .stack-more { opacity: 1; }

        /* ─── ROADMAP SECTION ─── */
        .roadmap {
            margin-top: 60px;
            position: relative;
            padding-left: 24px;
        }

        .roadmap::before {
            content: '';
            position: absolute;
            left: 24px;
            top: 12px;
            bottom: 12px;
            width: 2px;
            background: linear-gradient(to bottom, var(--accent), rgba(56, 189, 248, 0.3), rgba(56, 189, 248, 0.1), transparent);
        }

        .road-item {
            display: flex;
            gap: 32px;
            margin-bottom: 0;
            position: relative;
        }

        .road-left {
            position: absolute;
            left: -33px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .road-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 3px solid var(--border-bright);
            background: var(--bg);
            position: relative;
            z-index: 2;
            flex-shrink: 0;
            margin-top: 4px;
            transition: var(--transition-smooth);
        }

        .road-dot.done {
            background: var(--accent);
            border-color: var(--accent);
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
        }

        .road-dot.active {
            background: var(--accent2);
            border-color: var(--accent2);
            box-shadow: 0 0 16px rgba(129, 140, 248, 0.6);
            animation: pulse-dot 2s ease-in-out infinite;
        }

        .road-dot.soon { border-color: rgba(251, 191, 36, 0.5); }

        .road-body {
            padding-bottom: 48px;
            padding-left: 12px;
            flex: 1;
        }

        .road-phase {
            font-family: var(--mono);
            font-size: 0.6rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
        }

        .road-status-done { color: var(--accent3); }
        .road-status-active { color: var(--accent2); }
        .road-status-upcoming { color: var(--muted); }

        .road-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 8px;
        }

        .road-desc {
            font-family: var(--mono);
            font-size: 0.75rem;
            color: var(--muted2);
            line-height: 1.7;
        }

        .road-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 14px;
        }

        .road-chip {
            font-family: var(--mono);
            font-size: 0.55rem;
            letter-spacing: 0.06em;
            color: var(--muted);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 4px 10px;
            border-radius: 6px;
        }

        /* ─── ABOUT SECTION ─── */
        .about-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-top: 50px;
        }

        @media (max-width: 768px) { .about-grid { grid-template-columns: 1fr; } }

        .term-bio {
            background: rgba(8, 15, 31, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
        }

        .tb-titlebar {
            background: rgba(3, 7, 18, 0.95);
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .tb-dot { width: 12px; height: 12px; border-radius: 50%; }
        .tb-label {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: rgba(148, 163, 184, 0.5);
            margin-left: 8px;
            letter-spacing: 0.08em;
        }

        .tb-body {
            padding: 28px;
            font-family: var(--mono);
            font-size: 0.8rem;
            color: var(--muted2);
            line-height: 1.7;
        }

        .tb-pfp-row {
            display: flex;
            align-items: center;
            gap: 24px;
            margin-bottom: 24px;
        }

        .tb-pfp, .tb-pfp-placeholder {
            width: 88px;
            height: 88px;
            border-radius: 50%;
            border: 2px solid var(--accent);
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.4);
            flex-shrink: 0;
            object-fit: cover;
        }

        .tb-pfp-placeholder {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(167, 139, 250, 0.2));
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--mono);
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--accent);
        }

        .tb-name {
            color: var(--text);
            font-size: 1.1rem;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .tb-handle {
            color: var(--accent);
            font-size: 0.7rem;
        }

        .tb-loc {
            font-size: 0.65rem;
            color: var(--muted);
            margin-top: 4px;
        }

        .tb-list {
            list-style: none;
            margin: 20px 0;
        }

        .tb-list li {
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 0.75rem;
        }

        .tb-list li::before {
            content: '$';
            color: var(--accent3);
            flex-shrink: 0;
            font-weight: 700;
        }

        .tag-cloud {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }

        .tag {
            font-family: var(--mono);
            font-size: 0.6rem;
            color: var(--muted2);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 6px 12px;
            border-radius: 6px;
            letter-spacing: 0.05em;
            transition: var(--transition-smooth);
            text-transform: uppercase;
            cursor: default;
        }

        .tag:hover {
            border-color: rgba(56, 189, 248, 0.4);
            color: var(--accent);
            background: rgba(56, 189, 248, 0.05);
        }

        .about-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 26px;
            margin-bottom: 20px;
        }

        .about-box-title {
            font-family: var(--mono);
            font-size: 0.65rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            font-weight: 700;
        }

        .about-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .about-list li {
            font-size: 0.9rem;
            color: var(--muted2);
            display: flex;
            align-items: flex-start;
            gap: 12px;
            line-height: 1.6;
        }

        .about-list li::before {
            content: '→';
            color: var(--accent);
            font-family: var(--mono);
            font-size: 0.85rem;
            margin-top: 2px;
            flex-shrink: 0;
            font-weight: 700;
        }

        .about-list li > span {
            display: block;
            flex: 1;
            min-width: 0;
        }

        .about-list li > span strong {
            color: var(--text);
            font-weight: 600;
        }

        .cert-card {
            display: flex;
            align-items: center;
            gap: 18px;
            background: rgba(52, 211, 153, 0.05);
            border: 1px solid rgba(52, 211, 153, 0.2);
            padding: 22px 24px;
            border-radius: 12px;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            transition: var(--transition-smooth);
        }

        .cert-card:hover {
            border-color: rgba(52, 211, 153, 0.4);
            box-shadow: 0 10px 20px rgba(52, 211, 153, 0.05);
        }

        .cert-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: var(--accent3);
            border-radius: 0 2px 2px 0;
        }

        .cert-badge {
            font-family: var(--mono);
            font-size: 0.65rem;
            font-weight: 800;
            color: var(--accent3);
            background: rgba(52, 211, 153, 0.1);
            padding: 10px 14px;
            border-radius: 8px;
            border: 1px solid rgba(52, 211, 153, 0.2);
            flex-shrink: 0;
        }

        .cert-title {
            font-weight: 800;
            font-size: 1rem;
            color: var(--text);
            margin-bottom: 4px;
        }

        .cert-meta {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--muted2);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .cert-date {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--accent3);
            margin-top: 4px;
        }

        .cert-link {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--accent);
            text-decoration: none;
            margin-top: 8px;
            display: inline-block;
            font-weight: 700;
        }

        .cert-link:hover { text-decoration: underline; }

        /* ─── FOOTER & AUTHOR SECTION ─── */
        .author-section {
            border-top: 1px solid var(--border);
            background: var(--bg2);
        }

        .author-inner {
            max-width: 1120px;
            margin: 0 auto;
            padding: 90px 32px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 20px;
        }

        .author-pfp, .author-pfp-placeholder {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 2px solid var(--accent);
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.4);
            object-fit: cover;
        }

        .author-pfp-placeholder {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(167, 139, 250, 0.2));
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--mono);
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--accent);
        }

        .author-name {
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--text);
        }

        .author-role {
            font-family: var(--mono);
            font-size: 0.65rem;
            color: var(--muted);
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .author-links {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
            margin-top: 12px;
        }

        .author-link {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-family: var(--mono);
            font-size: 0.65rem;
            text-decoration: none;
            padding: 10px 18px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.03);
            color: var(--muted2);
            transition: var(--transition-smooth);
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .author-link svg {
            width: 14px;
            height: 14px;
            fill: currentColor;
            flex-shrink: 0;
        }

        .author-link:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(56, 189, 248, 0.08);
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        footer {
            text-align: center;
            padding: 24px 24px;
            border-top: 1px solid var(--border);
            font-family: var(--mono);
            font-size: 0.6rem;
            color: rgba(148, 163, 184, 0.4);
            letter-spacing: 0.1em;
            background: var(--bg);
        }

        /* ─── SCROLLING DATA TICKER ─── */
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background: rgba(56, 189, 248, 0.05);
            border-top: 1px solid rgba(56, 189, 248, 0.15);
            border-bottom: 1px solid rgba(56, 189, 248, 0.15);
            padding: 10px 0;
            backdrop-filter: blur(8px);
        }

        .ticker-track {
            display: flex;
            gap: 0;
            animation: ticker 35s linear infinite;
            width: max-content;
        }

        .ticker-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: var(--mono);
            font-size: 0.65rem;
            color: rgba(56, 189, 248, 0.7);
            padding: 0 40px;
            letter-spacing: 0.08em;
            white-space: nowrap;
            font-weight: 700;
        }

        .ticker-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--accent3);
            box-shadow: 0 0 8px var(--accent3);
        }

        @keyframes ticker {
            from { transform: translateX(0); }
            to { transform: translateX(-50%); }
        }

        /* ─── FADE IN ANIMATIONS ─── */
        .fade-in {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.8s ease-out, transform 0.8s ease-out;
        }

        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .fade-in-delay-1 { transition-delay: 0.15s; }
        .fade-in-delay-2 { transition-delay: 0.3s; }
        .fade-in-delay-3 { transition-delay: 0.45s; }

        /* ─── RESPONSIVE DESIGN ─── */
        @media (max-width: 768px) {
            nav { padding: 0 20px; }
            .hero h1 { font-size: 3.2rem; }
            .section-inner { padding: 80px 24px; }
            .about-grid { grid-template-columns: 1fr; }
            .flow-pipeline { flex-direction: column; }
            .arch-detail-row { grid-template-columns: 1fr; }
            .stats-bar { flex-direction: column; border-radius: var(--radius); }
            .stat-item { border-right: none; border-bottom: 1px solid var(--border-bright); }
            .stat-item:last-child { border-bottom: none; }
        }
    </style>
</head>
<body>

<!-- NAVIGATION -->
<nav>
    <div class="nav-logo">
        <div class="nav-logo-dot"></div>
        Nexaura
    </div>
    <ul class="nav-links">
        <li><a href="#architecture">Arch</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#stack">Stack</a></li>
        <li><a href="#roadmap">Roadmap</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="https://github.com/Sam-Dev-161127" class="nav-cta" target="_blank">GitHub →</a></li>
    </ul>
</nav>

<!-- LIVE TICKER -->
<div class="ticker-wrap" style="position:fixed; top:64px; left:0; right:0; z-index:400">
    <div class="ticker-track">
        <span class="ticker-item"><span class="ticker-dot"></span>Nexaura v2.1.0 STABLE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>PHASE 2 — PERCEPTION LAYER ACTIVE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>PYTHON 3.11.9 · GEMINI PRO · DEEPFACE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>WAKE WORD ENGINE: PORCUPINE ONLINE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>MEMORY VAULT: SQLITE3 WAL MODE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>LOCAL LLM FALLBACK: OLLAMA READY</span>
        <span class="ticker-item"><span class="ticker-dot"></span>FLASK REMOTE: 192.168.x.x:5000</span>
        <span class="ticker-item"><span class="ticker-dot"></span>ELEVENLABS TTS: STREAM CONNECTED</span>
        <!-- Duplicated to enable smooth infinite scrolling -->
        <span class="ticker-item"><span class="ticker-dot"></span>Nexaura v2.1.0 STABLE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>PHASE 2 — PERCEPTION LAYER ACTIVE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>PYTHON 3.11.9 · GEMINI PRO · DEEPFACE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>WAKE WORD ENGINE: PORCUPINE ONLINE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>MEMORY VAULT: SQLITE3 WAL MODE</span>
        <span class="ticker-item"><span class="ticker-dot"></span>LOCAL LLM FALLBACK: OLLAMA READY</span>
        <span class="ticker-item"><span class="ticker-dot"></span>FLASK REMOTE: 192.168.x.x:5000</span>
        <span class="ticker-item"><span class="ticker-dot"></span>ELEVENLABS TTS: STREAM CONNECTED</span>
    </div>
</div>

<!-- HERO SECTION -->
<section class="hero" style="padding-top:160px">
    <canvas id="particles-canvas"></canvas>
    
    <div class="haze haze-1"></div>
    <div class="haze haze-2"></div>
    <div class="haze haze-3"></div>

    <div class="hero-badge fade-in" style="position:relative; z-index:2">
        <span class="hero-badge-dot"></span>
        Phase 2 Active · Perception Layer Online
    </div>

    <h1 class="fade-in" style="position:relative; z-index:2">Nexaura</h1>
    <div class="hero-sub-line fade-in fade-in-delay-1" style="position:relative; z-index:2">Personal · AI · Operating · System</div>

    <p class="hero-desc fade-in fade-in-delay-2" style="position:relative; z-index:2">
        An intelligent, <strong>context-aware AI ecosystem</strong> that observes your environment, learns your workflow, and acts on your behalf — powered by <strong>Gemini Pro</strong> with persistent local memory.
    </p>

    <div class="hero-btns fade-in fade-in-delay-3" style="position:relative; z-index:2">
        <a class="btn-glow" href="#architecture">Explore Architecture</a>
        <a class="btn-ghost" href="#features">View Features</a>
        <a class="btn-ghost" href="https://github.com/Sam-Dev-161127" target="_blank">GitHub ↗</a>
    </div>

    <!-- Stats Panel -->
    <div class="stats-bar fade-in" style="position:relative; z-index:2">
        <div class="stat-item">
            <div class="stat-num" id="stat-latency"><span>~</span>140<span>ms</span></div>
            <div class="stat-label">Avg Response</div>
        </div>
        <div class="stat-item">
            <div class="stat-num"><span>9</span></div>
            <div class="stat-label">Core Modules</div>
        </div>
        <div class="stat-item">
            <div class="stat-num"><span>0</span> bytes</div>
            <div class="stat-label">Data Leaving Device</div>
        </div>
        <div class="stat-item">
            <div class="stat-num"><span>&lt;</span>1<span>%</span></div>
            <div class="stat-label">Idle CPU Usage</div>
        </div>
    </div>

    <!-- Typewriter Terminal -->
    <div class="terminal-wrap fade-in" style="position:relative; z-index:2">
        <div class="terminal-glow-ring"></div>
        <div class="terminal-glow-ring-inner">
            <div class="terminal">
                <div class="t-bar">
                    <div class="t-dot t-red"></div>
                    <div class="t-dot t-yellow"></div>
                    <div class="t-dot t-green"></div>
                    <div class="t-title">nexaura — main.py · python3.11</div>
                    <div class="t-tabs">
                        <div class="t-tab active">main.py</div>
                        <div class="t-tab">config.py</div>
                        <div class="t-tab">memory.py</div>
                    </div>
                </div>
                <div class="t-body" id="terminal-body">
                    <!-- Populated dynamically via JS typewriter effect -->
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ARCHITECTURE SECTION -->
<section id="architecture" style="background:var(--bg2); border-top:1px solid var(--border)">
    <div class="section-inner">
        <div class="section-eyebrow">System Architecture</div>
        <div class="section-title">Development Pipeline</div>
        <p class="section-sub">Nexaura follows a strict four-stage data pipeline from environment setup to cognitive output. Each stage is independently testable and extensible.</p>

        <div class="arch-container fade-in">
            <div class="arch-bg">
                <div class="flow-pipeline">
                    <!-- Node 1: IDE -->
                    <div class="flow-node" onclick="openModal('ide')" style="--node-color:#fcd34d">
                        <div class="fn-tag fn-amber">[ IDE ]</div>
                        <div class="fn-meta">Stage 01 · Setup</div>
                        <div class="fn-title">PyCharm Professional</div>
                        <div class="fn-desc">Project indexing, vEnv management, and intelligent autocompletion for Gemini SDK and DeepFace libraries.</div>
                        <div class="fn-more">Read IDE Docs →</div>
                    </div>
                    
                    <div class="flow-arrow">→</div>

                    <!-- Node 2: ENV -->
                    <div class="flow-node" onclick="openModal('env')" style="--node-color:#7dd3fc">
                        <div class="fn-tag fn-blue">[ ENV ]</div>
                        <div class="fn-meta">Stage 02 · Runtime</div>
                        <div class="fn-title">Python 3.11.9 vEnv</div>
                        <div class="fn-desc">Isolated virtual environment with CPython's adaptive specializing interpreter for 60% threading performance gains.</div>
                        <div class="fn-more">Read ENV Docs →</div>
                    </div>
                    
                    <div class="flow-arrow">→</div>

                    <!-- Node 3: DAT -->
                    <div class="flow-node" onclick="openModal('dat')" style="--node-color:#6ee7b7">
                        <div class="fn-tag fn-green">[ DAT ]</div>
                        <div class="fn-meta">Stage 03 · Sensing</div>
                        <div class="fn-title">Multimodal Input Layer</div>
                        <div class="fn-desc">DeepFace vision, Porcupine wake word, OpenCV streams, and SQLite WAL mode operating in parallel threads.</div>
                        <div class="fn-more">Read DAT Docs →</div>
                    </div>
                    
                    <div class="flow-arrow">→</div>

                    <!-- Node 4: LOG -->
                    <div class="flow-node" onclick="openModal('log')" style="--node-color:#c4b5fd">
                        <div class="fn-tag fn-purple">[ LOG ]</div>
                        <div class="fn-meta">Stage 04 · Cognition</div>
                        <div class="fn-title">Gemini Logic Engine</div>
                        <div class="fn-desc">Multimodal context injection into Gemini Pro with strict JSON output enforcement for deterministic OS automation.</div>
                        <div class="fn-more">Read LOG Docs →</div>
                    </div>
                </div>

                <!-- Architectural Details -->
                <div class="arch-detail-row" style="margin-top:24px">
                    <div class="arch-detail-card">
                        <div class="adc-label">Input Layer</div>
                        <div class="adc-title">Audio → Porcupine STT</div>
                        <div class="adc-desc">Edge-computed acoustic wake word triggering near-zero CPU interrupt on voice activation.</div>
                    </div>
                    <div class="arch-detail-card">
                        <div class="adc-label">Vision Layer</div>
                        <div class="adc-title">Camera → DeepFace CNN</div>
                        <div class="adc-desc">Non-blocking 10fps BGR frame sampling, emotion logit array cached in global state.</div>
                    </div>
                    <div class="arch-detail-card">
                        <div class="adc-label">Memory Layer</div>
                        <div class="adc-title">SQLite3 WAL Vault</div>
                        <div class="adc-desc">Asynchronous read/write with LRU cache; context serialized as JSON blobs for LLM injection.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- FEATURES SECTION -->
<section id="features">
    <div class="section-inner">
        <div class="section-eyebrow">System Capabilities</div>
        <div class="section-title">The Nexaura Feature Suite</div>
        <p class="section-sub">Nine production-grade modules working in concert. Click any card to read full technical documentation and integration guides.</p>

        <div class="features-grid">
            <!-- Memory Feature -->
            <div class="feat-card fade-in fade-in-delay-1" onclick="openModal('memory')">
                <div class="feat-top-bar" style="--feat-color:var(--accent)"></div>
                <div class="feat-badge fb-blue">[ MEM ] Memory</div>
                <div class="feat-title">Persistent Context Memory</div>
                <div class="feat-desc">SQLite3 vault with Write-Ahead Logging builds a dynamic interaction graph — habits, tool preferences, and workflow sequences, all persisted across sessions.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- Wake Word Feature -->
            <div class="feat-card fade-in fade-in-delay-2" onclick="openModal('wake')">
                <div class="feat-top-bar" style="--feat-color:#a78bfa"></div>
                <div class="feat-badge fb-purple">[ MIC ] Audio</div>
                <div class="feat-title">Porcupine Wake Word Engine</div>
                <div class="feat-desc">Picovoice Porcupine runs entirely on-device using cross-correlation acoustic modeling. Zero audio bytes leave the machine before the interrupt threshold is triggered.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- Emotion Recognition Feature -->
            <div class="feat-card fade-in fade-in-delay-3" onclick="openModal('emotion')">
                <div class="feat-top-bar" style="--feat-color:#34d399"></div>
                <div class="feat-badge fb-green">[ VIS ] Vision</div>
                <div class="feat-title">DeepFace Emotion Recognition</div>
                <div class="feat-desc">CNN-based facial landmark analysis via VGG-Face/Facenet models sampling at 10fps. Emotion state injected into Gemini system prompt for adaptive tone modulation.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- Plugins Feature -->
            <div class="feat-card fade-in" onclick="openModal('plugins')">
                <div class="feat-top-bar" style="--feat-color:#fb923c"></div>
                <div class="feat-badge fb-amber">[ EXT ] Extension</div>
                <div class="feat-title">Plugin Hot-Reloading</div>
                <div class="feat-desc">Watchdog monitors /plugins/ directory via importlib and os.walk. New Python modules dynamically mounted into the OS namespace with strict error boundaries preventing core crashes.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- OS Automation Feature -->
            <div class="feat-card fade-in" onclick="openModal('os')">
                <div class="feat-top-bar" style="--feat-color:#f87171"></div>
                <div class="feat-badge fb-red">[ CMD ] Control</div>
                <div class="feat-title">OS Automation Hub</div>
                <div class="feat-desc">NLP-to-system-interrupt translation via PyAutoGUI and subprocess. Maps display resolutions, emulates keyboard hardware, executes template-matched mouse clicks and shell pipelines.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- Mobile Remote Feature -->
            <div class="feat-card fade-in" onclick="openModal('mobile')">
                <div class="feat-top-bar" style="--feat-color:#2dd4bf"></div>
                <div class="feat-badge fb-teal">[ NET ] Network</div>
                <div class="feat-title">Flask Mobile Remote</div>
                <div class="feat-desc">Lightweight Werkzeug WSGI server on a background thread, bound to 0.0.0.0:5000. Exposes RESTful endpoints for remote command execution over local subnet.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- Voice TTS Feature -->
            <div class="feat-card fade-in" onclick="openModal('voice')">
                <div class="feat-top-bar" style="--feat-color:var(--accent)"></div>
                <div class="feat-badge fb-blue">[ VOC ] Voice</div>
                <div class="feat-title">ElevenLabs Neural TTS</div>
                <div class="feat-desc">Studio-grade neural speech synthesis bypassing legacy pyttsx3/SAPI5 engines. Stability, similarity_boost, and style scaling are programmatically controlled per emotional context.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- Security Feature -->
            <div class="feat-card fade-in" onclick="openModal('security')">
                <div class="feat-top-bar" style="--feat-color:#6ee7b7"></div>
                <div class="feat-badge fb-green">[ SEC ] Security</div>
                <div class="feat-title">Air-Gapped Local Execution</div>
                <div class="feat-desc">Wake word modeling, facial CNN matrices, and SQLite graph construction run entirely on edge hardware. Only sanitized NLP text reaches external APIs — zero raw sensor data egress.</div>
                <div class="feat-footer">
                    <div class="feat-status">● Active</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>

            <!-- Local LLM Fallback -->
            <div class="feat-card fade-in" onclick="openModal('local_llm')">
                <div class="feat-top-bar" style="--feat-color:#c4b5fd"></div>
                <div class="feat-badge fb-purple">[ LCL ] Fallback</div>
                <div class="feat-title">Local LLM via Ollama</div>
                <div class="feat-desc">Automatic failover routing to quantized local models (Llama 3 8B) via Ollama daemon when Gemini API times out or the device goes air-gapped. Transparent to the user.</div>
                <div class="feat-footer">
                    <div class="feat-status feat-status-inactive">○ Standby</div>
                    <div class="feat-detail-btn">Read Docs →</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- TECH STACK SECTION -->
<div class="stack-section">
    <section id="stack">
        <div class="section-inner">
            <div class="section-eyebrow">Technology</div>
            <div class="section-title">System Stack</div>
            <p class="section-sub">Every library and framework selected for minimum overhead and maximum reliability on local edge hardware.</p>

            <div class="stack-grid fade-in">
                <div class="stack-card" onclick="openModal('stack_engine')">
                    <div class="stack-cat">Engine</div>
                    <div class="stack-name">Python 3.11.9</div>
                    <div class="stack-ver">CPython Stable</div>
                    <div class="stack-role">Adaptive Specializing Interpreter</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_ai')">
                    <div class="stack-cat">AI Brain</div>
                    <div class="stack-name">Gemini Pro</div>
                    <div class="stack-ver">google-generativeai SDK</div>
                    <div class="stack-role">Multimodal LLM · JSON Output</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_vision')">
                    <div class="stack-cat">Vision CNN</div>
                    <div class="stack-name">DeepFace</div>
                    <div class="stack-ver">VGG-Face / Facenet</div>
                    <div class="stack-role">Emotion · Identity Recognition</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_db')">
                    <div class="stack-cat">Persistence</div>
                    <div class="stack-name">SQLite3</div>
                    <div class="stack-ver">WAL Mode Enabled</div>
                    <div class="stack-role">Async Memory Vault</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_ui')">
                    <div class="stack-cat">Desktop GUI</div>
                    <div class="stack-name">PyQt6</div>
                    <div class="stack-ver">Qt C++ Bindings</div>
                    <div class="stack-role">GPU-Accelerated Overlay</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_net')">
                    <div class="stack-cat">Remote API</div>
                    <div class="stack-name">Flask + Werkzeug</div>
                    <div class="stack-ver">WSGI Server</div>
                    <div class="stack-role">Mobile REST Endpoint</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                
                <div class="stack-card" onclick="openModal('stack_sr')">
                    <div class="stack-cat">Audio Input</div>
                    <div class="stack-name">SpeechRecognition</div>
                    <div class="stack-ver">Python Module</div>
                    <div class="stack-role">Voice-to-Text Conversion</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_tts')">
                    <div class="stack-cat">Offline TTS</div>
                    <div class="stack-name">pyttsx3</div>
                    <div class="stack-ver">SAPI5 Engine</div>
                    <div class="stack-role">Text-to-Speech Output</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_env')">
                    <div class="stack-cat">Security</div>
                    <div class="stack-name">python-dotenv</div>
                    <div class="stack-ver">Config Manager</div>
                    <div class="stack-role">API Key Management</div>
                    <div class="stack-more">View Docs →</div>
                </div>

                <!-- NEW STACK CARDS EXTRACTED FROM NEXAURA FEATURES -->
                <div class="stack-card" onclick="openModal('stack_webbrowser')">
                    <div class="stack-cat">Web Control</div>
                    <div class="stack-name">webbrowser</div>
                    <div class="stack-ver">Python Std Library</div>
                    <div class="stack-role">Automated Site Navigation</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_requests')">
                    <div class="stack-cat">Network</div>
                    <div class="stack-name">requests</div>
                    <div class="stack-ver">HTTP Library</div>
                    <div class="stack-role">Fetch Info & APIs</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <div class="stack-card" onclick="openModal('stack_os')">
                    <div class="stack-cat">System OS</div>
                    <div class="stack-name">os</div>
                    <div class="stack-ver">Python Std Library</div>
                    <div class="stack-role">Launch Desktop Apps</div>
                    <div class="stack-more">View Docs →</div>
                </div>
                <!-- END OF NEW CARDS -->

            </div>
        </div>
    </section>
</div>

<!-- ROADMAP SECTION -->
<section id="roadmap" style="background:var(--bg2); border-top:1px solid var(--border)">
    <div class="section-inner">
        <div class="section-eyebrow">Vision</div>
        <div class="section-title">Nexaura Roadmap</div>
        <p class="section-sub">Five-phase evolution from a local AI assistant to a full physical-world operating system.</p>

        <div class="roadmap fade-in">
            <!-- Phase 1 -->
            <div class="road-item">
                <div class="road-left">
                    <div class="road-dot done"></div>
                </div>
                <div class="road-body">
                    <div class="road-phase road-status-done">Phase 1 · Foundation <span>✓ COMPLETED</span></div>
                    <div class="road-title">Core OS Architecture</div>
                    <div class="road-desc">Stable Python 3.11 build, SQLite memory integration, basic voice-to-action pipeline, PyCharm development environment, and initial Gemini API routing.</div>
                    <div class="road-chips">
                        <span class="road-chip">Python 3.11.9</span>
                        <span class="road-chip">SQLite3 Vault</span>
                        <span class="road-chip">Gemini API</span>
                        <span class="road-chip">ElevenLabs TTS</span>
                    </div>
                </div>
            </div>

            <!-- Phase 2 -->
            <div class="road-item" style="margin-top:40px">
                <div class="road-left">
                    <div class="road-dot active"></div>
                </div>
                <div class="road-body">
                    <div class="road-phase road-status-active">Phase 2 · Perception <span>◉ IN PROGRESS</span></div>
                    <div class="road-title">Advanced Sensing Layer</div>
                    <div class="road-desc">DeepFace emotion tracking, Porcupine wake word engine, MediaPipe gesture control, and multimodal context injection into the Gemini prompt pipeline.</div>
                    <div class="road-chips">
                        <span class="road-chip">DeepFace CNN</span>
                        <span class="road-chip">Porcupine STT</span>
                        <span class="road-chip">MediaPipe</span>
                        <span class="road-chip">Context Injection</span>
                    </div>
                </div>
            </div>

            <!-- Phase 3 -->
            <div class="road-item" style="margin-top:40px">
                <div class="road-left">
                    <div class="road-dot soon"></div>
                </div>
                <div class="road-body">
                    <div class="road-phase road-status-upcoming">Phase 3 · Integration <span>· UPCOMING</span></div>
                    <div class="road-title">Universal Plugin Marketplace</div>
                    <div class="road-desc">Hot-reloadable community plugin ecosystem with sandboxed execution. Planned connectors: Weather, Stocks, Spotify, IDE control, Smart Home, and Calendar sync.</div>
                    <div class="road-chips">
                        <span class="road-chip">Plugin SDK</span>
                        <span class="road-chip">Watchdog FS</span>
                        <span class="road-chip">Sandboxing</span>
                        <span class="road-chip">Community Hub</span>
                    </div>
                </div>
            </div>

            <!-- Phase 4 -->
            <div class="road-item" style="margin-top:40px">
                <div class="road-left">
                    <div class="road-dot"></div>
                </div>
                <div class="road-body">
                    <div class="road-phase road-status-upcoming">Phase 4 · Intelligence <span>· PLANNED</span></div>
                    <div class="road-title">Behavioral Prediction Engine</div>
                    <div class="road-desc">AI proactively predicts workflow needs based on time-of-day, historical SQLite patterns, and biometric state. Nexaura acts before you ask.</div>
                    <div class="road-chips">
                        <span class="road-chip">Time-Series Analysis</span>
                        <span class="road-chip">Pattern Recognition</span>
                        <span class="road-chip">Proactive Actions</span>
                    </div>
                </div>
            </div>

            <!-- Phase 5 -->
            <div class="road-item" style="margin-top:40px">
                <div class="road-left">
                    <div class="road-dot"></div>
                </div>
                <div class="road-body">
                    <div class="road-phase road-status-upcoming">Phase 5 · Physical <span>· FUTURE</span></div>
                    <div class="road-title">Hardware &amp; Robotics Integration</div>
                    <div class="road-desc">Raspberry Pi 5 edge deployment, Arduino sensor networks, IoT device control, and robotic arm actuation — bridging the digital OS into physical space.</div>
                    <div class="road-chips">
                        <span class="road-chip">Raspberry Pi 5</span>
                        <span class="road-chip">Arduino I/O</span>
                        <span class="road-chip">IoT Mesh</span>
                        <span class="road-chip">Robotics</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ABOUT SECTION -->
<section id="about">
    <div class="section-inner">
        <div class="section-eyebrow">Developer</div>
        <div class="section-title">About the Builder</div>

        <div class="about-grid fade-in">
            <!-- Left Column: Terminal Bio & Directives -->
            <div>
                <div class="term-bio">
                    <div class="tb-titlebar">
                        <span class="tb-dot" style="background:#ff5f57"></span>
                        <span class="tb-dot" style="background:#febc2e"></span>
                        <span class="tb-dot" style="background:#28c840"></span>
                        <span class="tb-label">sameer@nexaura:~$ whoami --verbose</span>
                    </div>
                    <div class="tb-body">
                        <div class="tb-pfp-row">
                            <img src="pfp.png" alt="Sameer Patra" class="tb-pfp" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                            <div class="tb-pfp-placeholder" style="display:none;">SP</div>
                            <div>
                                <div class="tb-name">Sameer Patra</div>
                                <div class="tb-handle">@Sam-Dev-161127</div>
                                <div class="tb-loc">📍 Balasore, Odisha, India</div>
                                <div style="margin-top:6px; font-size:0.62rem; color:var(--accent)">
                                    <a href="mailto:sam.dev1611@gmail.com" style="color:inherit; text-decoration:none">sam.dev1611@gmail.com</a>
                                </div>
                            </div>
                        </div>
                        <ul class="tb-list">
                            <li>Student developer — engineering since 2024</li>
                            <li>Focus: Python · Web Dev · Robotics · AI</li>
                            <li>Building physics games in Godot Engine</li>
                            <li>NIELIT AI/ML Internship graduate</li>
                            <li>Goal: Become an engineer who ships real things</li>
                        </ul>
                        <div class="tag-cloud">
                            <span class="tag">Godot Dev</span>
                            <span class="tag">Python</span>
                            <span class="tag">Linux Ubuntu</span>
                            <span class="tag">AI / ML</span>
                            <span class="tag">Robotics</span>
                            <span class="tag">Web Dev</span>
                        </div>
                    </div>
                </div>

                <div class="about-box" style="margin-top:20px; background:rgba(56,189,248,0.03); border-style:dashed; border-color:rgba(56,189,248,0.2)">
                    <div class="about-box-title">[ DIR ] Active Directives</div>
                    <ul class="about-list">
                        <li><span>Developing physics-based game mechanics in <strong>Godot Engine</strong></span></li>
                        <li><span>Mastering async patterns in <strong>Python 3.11</strong></span></li>
                        <li><span>Exploring embedded systems and <strong>Robotics</strong></span></li>
                        <li><span>Studying <strong>Mathematics</strong> for algorithm design</span></li>
                    </ul>
                </div>
            </div>

            <!-- Right Column: Certifications & Skills -->
            <div>
                <div class="cert-card">
                    <div class="cert-badge">CERT</div>
                    <div>
                        <div class="cert-title">Crash Course on Python</div>
                        <div class="cert-meta">Authorized by Google · Coursera</div>
                        <div class="cert-date">✓ Completed: May 11, 2026</div>
                        <a href="https://coursera.org/verify/IKPW8JE4BPJP" target="_blank" class="cert-link">Verify Credential →</a>
                    </div>
                </div>

                <div class="about-box">
                    <div class="about-box-title">Achievements</div>
                    <ul class="about-list">
                        <li><span>Completed a <strong>5-Day NIELIT Internship</strong> on AI &amp; Machine Learning using Python.</span></li>
                        <li><span>Built beginner-level <strong>AI assistant and automation</strong> projects independently.</span></li>
                        <li><span>Proficient in <strong>VS Code, PyCharm</strong>, and modern development tooling.</span></li>
                        <li><span>Passionate about <strong>robotics</strong> and innovative engineering.</span></li>
                        <li><span>Skilled in <strong>Canva and PowerPoint</strong> for technical presentation design.</span></li>
                    </ul>
                </div>

                <div class="about-box">
                    <div class="about-box-title">Technical Skills &amp; Tools</div>
                    <div class="tag-cloud">
                        <span class="tag">Python</span>
                        <span class="tag">Godot Engine</span>
                        <span class="tag">PyCharm</span>
                        <span class="tag">VS Code</span>
                        <span class="tag">Linux</span>
                        <span class="tag">AI / ML Basics</span>
                        <span class="tag">Git &amp; GitHub</span>
                        <span class="tag">Web Dev</span>
                        <span class="tag">Canva</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- AUTHOR FOOTER SECTION -->
<section class="author-section">
    <div class="author-inner">
        <img src="pfp.png" class="author-pfp" alt="Sameer Patra" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="author-pfp-placeholder" style="display:none;">SP</div>
        <div class="author-name">Sameer Patra</div>
        <div class="author-role">// lead architect · nexaura systems · 2026</div>
        
        <div class="author-links">
            <a class="author-link" href="https://github.com/Sam-Dev-161127" target="_blank">
                <svg viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.285 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                GitHub
            </a>
            <a class="author-link" href="https://www.linkedin.com/in/sameer-patra-2b17a83a7" target="_blank">
                <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                LinkedIn
            </a>
            <a class="author-link" href="https://x.com/Sam_Dev_161127" target="_blank">
                <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                Twitter / X
            </a>
            <a class="author-link" href="https://www.instagram.com/sam.dev.161127" target="_blank">
                <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                Instagram
            </a>
            <a class="author-link" href="https://t.me/Sameer161127" target="_blank">
                <svg viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 12 0 0012 0a12 12 0 00-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 01.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.892-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
                Telegram
            </a>
        </div>
    </div>
</section>

<footer>⬡ NEXAURA SYSTEMS &nbsp;·&nbsp; BUILT IN PYTHON 3.11.9 &nbsp;·&nbsp; SAMEER PATRA &nbsp;·&nbsp; 2026</footer>

<!-- DYNAMIC MODAL -->
<div class="modal-overlay" id="featureModal">
    <div class="modal-content">
        <div class="modal-close" onclick="closeModal()">[ ESC ]</div>
        <div class="modal-head">
            <div class="modal-icon-box feat-badge" id="m-icon" style="margin:0"></div>
            <div class="modal-info">
                <div class="modal-title" id="m-title"></div>
                <div class="modal-sub" id="m-sub"></div>
            </div>
        </div>
        <div class="modal-body" id="m-desc"></div>
        <div class="modal-section-label">Technical Integration Guide</div>
        <div class="modal-code-block" id="m-usage"></div>
        <div class="modal-tags" id="m-tags"></div>
    </div>
</div>

<script>
    // ─── PARTICLE BACKGROUND SYSTEM ───
    const canvas = document.getElementById('particles-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let W, H;

    function resize() {
        W = canvas.width = canvas.offsetWidth;
        H = canvas.height = canvas.offsetHeight;
    }

    function createParticle() {
        return {
            x: Math.random() * W,
            y: Math.random() * H,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            r: Math.random() * 2 + 0.5,
            opacity: Math.random() * 0.5 + 0.1,
            color: Math.random() > 0.6 ? '56,189,248' : Math.random() > 0.5 ? '129,140,248' : '52,211,153'
        };
    }

    resize();
    window.addEventListener('resize', () => { 
        resize(); 
        particles = Array.from({length: 100}, createParticle); 
    });
    
    particles = Array.from({length: 100}, createParticle);

    function animateParticles() {
        ctx.clearRect(0, 0, W, H);
        particles.forEach((p, i) => {
            p.x += p.vx; 
            p.y += p.vy;
            
            // Screen wrapping
            if(p.x < 0) p.x = W; 
            if(p.x > W) p.x = 0;
            if(p.y < 0) p.y = H; 
            if(p.y > H) p.y = 0;
            
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${p.color}, ${p.opacity})`;
            ctx.fill();
            
            // Draw connecting lines
            particles.slice(i + 1).forEach(p2 => {
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if(dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(56, 189, 248, ${0.05 * (1 - dist / 120)})`;
                    ctx.lineWidth = 0.6;
                    ctx.stroke();
                }
            });
        });
        requestAnimationFrame(animateParticles);
    }
    animateParticles();

    // ─── TYPEWRITER TERMINAL EFFECT ───
    const termLines = [
        {type: 'dim', text: '# Nexaura OS Boot Sequence v2.1.0'},
        {type: 'prompt', cmd: 'python3 main.py --mode production'},
        {type: 'ok', text: '  [BOOT]  CPython 3.11.9 Adaptive Interpreter Online'},
        {type: 'ok', text: '  [MEM]   SQLite3 Vault Connected · WAL Mode Active'},
        {type: 'ok', text: '  [AUDIO] Porcupine Wake Engine Initialized'},
        {type: 'progress', label: '  [VIS]   Loading DeepFace CNN Models', pct: 100, color: 'b1'},
        {type: 'ok', text: '  [VIS]   DeepFace Ready · VGG-Face Backbone Active'},
        {type: 'progress', label: '  [AI]    Authenticating Gemini Pro API', pct: 100, color: 'b2'},
        {type: 'ok', text: '  [AI]    Gemini Pro Connected · JSON Mode Enabled'},
        {type: 'ok', text: '  [TTS]   ElevenLabs Neural Voice Stream Ready'},
        {type: 'sys', text: '  [NET]   Flask WSGI @ 192.168.1.105:5000 Online'},
        {type: 'sys', text: '  [LCL]   Ollama Fallback · llama3:8b Standby'},
        {type: 'warn', text: '  [WARN]  VISION_ACTIVE=True · Webcam Access Granted'},
        {type: 'sys', text: '  [SYS]   All 9 Modules Operational · Engine LIVE'},
        {type: 'prompt', cmd: ''},
    ];

    const tbody = document.getElementById('terminal-body');
    let li = 0;

    function renderLine(line) {
        const div = document.createElement('div');
        div.className = 't-line';
        if(line.type === 'prompt') {
            div.innerHTML = `<span class="t-prompt">❯ </span><span class="t-cmd">${line.cmd || ''}</span>${line.cmd === '' ? '<span class="t-cursor"></span>' : ''}`;
        } else if(line.type === 'progress') {
            div.innerHTML = `<span class="t-sys">${line.label}</span>`;
            tbody.appendChild(div);
            const pr = document.createElement('div');
            pr.className = 't-line t-progress';
            pr.innerHTML = `<span class="t-dim" style="font-size:0.6rem; flex-shrink:0">  ████</span><div class="t-bar-mini"><div class="t-bar-fill ${line.color}"></div></div><span class="t-ok" style="font-size:0.65rem; flex-shrink:0">100%</span>`;
            tbody.appendChild(pr);
            return;
        } else {
            const cls = {ok:'t-ok', sys:'t-sys', warn:'t-warn', err:'t-err', dim:'t-dim', highlight:'t-highlight'}[line.type] || 't-cmd';
            div.innerHTML = `<span class="${cls}">${line.text}</span>`;
        }
        tbody.appendChild(div);
        tbody.scrollTop = tbody.scrollHeight;
    }

    function nextLine() {
        if(li >= termLines.length) return;
        renderLine(termLines[li]);
        li++;
        setTimeout(nextLine, li === 1 ? 400 : li < 4 ? 250 : 150);
    }
    setTimeout(nextLine, 800);

    // ─── SCROLL FADE-IN OBSERVER ───
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if(e.isIntersecting) { 
                e.target.classList.add('visible'); 
                observer.unobserve(e.target); 
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

    // ─── MODAL DATA & LOGIC ───
    const modalData = {
        ide: {
            icon: '[ IDE ]', iconClass: 'fb-amber', title: 'PyCharm Professional Environment', sub: 'Stage 01 · IDE Setup',
            desc: `PyCharm provides an unparalleled development environment for Nexaura. Deep code indexing enables real-time PEP-8 inspection of asynchronous AI logic, seamless local database schema integration, and intelligent autocompletion for the Gemini SDK and DeepFace computational frameworks.\n\nBy marking the /core and /plugins directories as "Sources Root", PyCharm resolves all sys.path conflicts inherent to multi-module AI projects, ensuring accurate type-checking across the entire dependency tree.`,
            usage: `Step 1. Open the root Nexaura/ repository in PyCharm.\nStep 2. Navigate to: File → Settings → Build, Execution, Deployment\n        Enable "Background asynchronous compilation" for optimal indexing.\nStep 3. Right-click /core → Mark Directory As → Sources Root\nStep 4. Right-click /plugins → Mark Directory As → Sources Root\nStep 5. Configure the Python 3.11.9 interpreter (see ENV docs).\nStep 6. Open the embedded terminal (Alt+F12) and run:\n        pip install -r requirements.txt`,
            tags: ['PyCharm', 'PEP-8', 'Sources Root', 'Type Checking']
        },
        env: {
            icon: '[ ENV ]', iconClass: 'fb-blue', title: 'Python 3.11.9 Virtual Environment', sub: 'Stage 02 · Runtime Isolation',
            desc: `Nexaura mandates Python 3.11.9 specifically to leverage PEP 659 — the Specializing Adaptive Interpreter. This provides up to a 60% boost in runtime execution speed for intensive I/O-bound automation tasks compared to Python 3.9.\n\nThe virtual environment (vEnv) isolates system dependencies, preventing complex C++ path conflicts common with machine learning and computer vision libraries like OpenCV and DeepFace. This isolation is non-negotiable for consistent cross-platform behavior.`,
            usage: `# Initialize the isolated environment\npython -m venv venv\n\n# Activate (Linux/macOS)\nsource venv/bin/activate\n\n# Activate (Windows)\n.\\venv\\Scripts\\activate\n\n# Resolve the full dependency tree\npip install -r requirements.txt\n\n# Verify the interpreter version\npython --version  # Must output: Python 3.11.9`,
            tags: ['Python 3.11.9', 'CPython', 'PEP 659', 'vEnv', 'Dependency Isolation']
        },
        dat: {
            icon: '[ DAT ]', iconClass: 'fb-green', title: 'Multi-Modal Core Sensing Layer', sub: 'Stage 03 · Data Ingestion',
            desc: `The sensory ingestion layer continuously buffers local environmental data across multiple parallel threads. Three sub-systems operate concurrently:\n\n• Vision: OpenCV BGR frame extraction at 10fps → DeepFace CNN analysis → emotion logit array cached in global state.\n• Audio: PyAudio byte stream → Picovoice Porcupine acoustic modeling → 5-second command buffer activation.\n• Storage: SQLite3 WAL mode for asynchronous I/O — non-blocking simultaneous reads and writes using PRAGMA journal_mode=WAL.`,
            usage: `# Vision subsystem — grant hardware access\n# Ensure OS-level webcam permission is granted.\nimport cv2\ncap = cv2.VideoCapture(0)  # 0 = default camera\n\n# Audio subsystem — verify input device\nimport pvporcupine\nporcupine = pvporcupine.create(\n    access_key=ACCESS_KEY,\n    keywords=['nexaura']\n)\n\n# Storage — auto-initializes on cold boot\n# vault.db handles schema migrations automatically.\n# PRAGMA journal_mode=WAL is set on connection.`,
            tags: ['OpenCV', 'DeepFace', 'Porcupine', 'PyAudio', 'SQLite3 WAL']
        },
        log: {
            icon: '[ LOG ]', iconClass: 'fb-purple', title: 'Gemini Pro Logic Engine', sub: 'Stage 04 · Cognitive Processing',
            desc: `The Logic Engine is the central cognitive processor. It dynamically engineers prompts by concatenating user voice inputs, active emotion classification strings, and parsed SQLite historical context arrays. Generation parameters are strictly locked to enforce deterministic JSON output and prevent hallucinations in downstream OS automation.\n\nToken budgets are carefully controlled — the context window is engineered, not left to chance. System prompts include active emotional state, last 5 interactions, current time, and active plugin registry.`,
            usage: `# config.py — required environment bindings\nGEMINI_API_KEY = "your_key_from_ai.google.com"\nENGINE_MODE = "production"\nFALLBACK_MODEL = "llama3"\nENABLE_FALLBACK = True\n\n# Generation config — locked for determinism\ngeneration_config = {\n    "temperature": 0.2,\n    "response_mime_type": "application/json",\n    "max_output_tokens": 512\n}\n\n# Launch the core engine loop\npython3 main.py --mode production`,
            tags: ['Gemini Pro', 'JSON Mode', 'Prompt Engineering', 'Context Window', 'Deterministic Output']
        },
        memory: {
            icon: '[ MEM ]', iconClass: 'fb-blue', title: 'Persistent Context Memory Vault', sub: 'Feature · SQLite3 WAL Persistence',
            desc: `Unlike stateless chat clients, Nexaura engineers a localized relational memory graph. Interaction states, bash command frequencies, and conversational arrays are serialized as JSON blobs and committed to the SQLite3 vault.\n\nThe system uses Least Recently Used (LRU) cache methodology to surface the most contextually relevant historical interactions for each Gemini prompt injection. This means Nexaura remembers that you refactored a specific script three days ago — without you needing to repeat yourself.\n\nThree primary tables: interactions_log, preference_weights, active_plugins.`,
            usage: `# Query historical context (example)\n"Hey Nexaura, what was the Godot physics script I wrote last Tuesday?"\n# → Nexaura queries SQLite vault by timestamp + keyword matching\n# → Injects top 3 matches into Gemini context window\n\n# Manual context dump (CLI)\npython3 main.py --dump-memory --limit 20\n\n# Full memory purge\npython3 main.py --reset-memory\n\n# Direct DB inspection\nsqlite3 data/vault.db\n.tables\nSELECT * FROM interactions_log ORDER BY timestamp DESC LIMIT 10;`,
            tags: ['SQLite3', 'WAL Mode', 'LRU Cache', 'JSON Blobs', 'Context Injection']
        },
        wake: {
            icon: '[ MIC ]', iconClass: 'fb-purple', title: 'Porcupine Wake Word Engine', sub: 'Feature · Edge Audio Processing',
            desc: `The audio interception pipeline uses the Picovoice Porcupine framework running on a dedicated I/O audio daemon thread. Cross-correlation acoustic modeling runs entirely on local CPU/edge hardware.\n\nThis ensures an ultra-low CPU footprint (under 1% idle) and absolute zero-trust privacy — no audio bytes leave the local machine until the interrupt threshold is mathematically triggered. The detection threshold, sensitivity, and acoustic model are all configurable per hardware environment.`,
            usage: `# Porcupine initialization\nimport pvporcupine\n\nporcupine = pvporcupine.create(\n    access_key=os.environ['PICOVOICE_KEY'],\n    keywords=['nexaura'],\n    sensitivities=[0.7]  # 0.0–1.0 (higher = more sensitive)\n)\n\n# Audio callback loop (runs on daemon thread)\n# On detection → 5-second voice capture begins\n# Confirmed by a sinusoidal tone at 880Hz\n\n# Wake phrase: "Hey Nexaura"`,
            tags: ['Picovoice', 'Porcupine', 'Edge Compute', 'Daemon Thread', 'Zero Data Egress']
        },
        emotion: {
            icon: '[ VIS ]', iconClass: 'fb-green', title: 'DeepFace Emotion Recognition', sub: 'Feature · CNN Vision Analysis',
            desc: `The vision subsystem intercepts raw BGR webcam frames at 10fps via OpenCV's VideoCapture, passing them through a Convolutional Neural Network via the DeepFace library (VGG-Face / Facenet backbone).\n\nEmotion logit arrays are computed across 7 states: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral. The dominant emotion string is cached in global state and injected into the Gemini system prompt, dynamically adjusting tone and verbosity.\n\nWhen high "stress" tensors are detected, Nexaura restricts verbose output and optimizes for concise, solution-oriented responses.`,
            usage: `# Vision config (config.py)\nVISION_ACTIVE = True\nVISION_SAMPLE_INTERVAL = 10  # seconds between samples\n\n# Internal processing pipeline:\n# 1. cap = cv2.VideoCapture(0)\n# 2. ret, frame = cap.read()  # BGR matrix\n# 3. result = DeepFace.analyze(\n#      frame,\n#      enforce_detection=False,\n#      actions=['emotion']\n#    )\n# 4. dominant = result[0]['dominant_emotion']\n# 5. Cached in global EMOTIONAL_STATE for Gemini\n\n# Tip: Stay in webcam view for complex commands.`,
            tags: ['DeepFace', 'OpenCV', 'VGG-Face', 'Facenet', 'CNN', 'Emotion Logits']
        },
        plugins: {
            icon: '[ EXT ]', iconClass: 'fb-amber', title: 'Plugin Hot-Reload Architecture', sub: 'Feature · Dynamic Module Loading',
            desc: `Nexaura is built on an extensible, decoupled architecture. A Watchdog daemon monitors the /plugins/ directory using Python's native importlib and os.walk. When a new .py module is detected, it is dynamically mounted into the OS namespace — no restart required.\n\nEach plugin is wrapped in strict error boundaries. A crash inside a plugin cannot propagate to the core loop. The plugin is registered into the available intent dictionary matrix, and Gemini can then route NLP queries to it.`,
            usage: `# Plugin boilerplate (system_monitor.py)\n# Place any file matching this signature in /plugins/\n\ndef handle(query: str) -> str:\n    """\n    Nexaura will call this function when it routes\n    a user query to your plugin.\n    """\n    if "cpu" in query.lower():\n        import psutil\n        return f"CPU usage: {psutil.cpu_percent()}%"\n    return "Unknown query."\n\n# Console output on detection:\n# [SYS] Namespace updated.\n# [SYS] Plugin registered: system_monitor`,
            tags: ['importlib', 'Watchdog', 'Hot-Reload', 'Error Boundaries', 'Plugin SDK']
        },
        os: {
            icon: '[ CMD ]', iconClass: 'fb-red', title: 'OS Automation Hub', sub: 'Feature · System-Level Control',
            desc: `Acting as the physical execution layer, Nexaura translates NLP intents into raw system-level interrupts. PyAutoGUI and subprocess libraries map display resolutions, emulate hardware keyboard keystrokes, execute template-matched mouse clicks, and manage complex shell application environments.\n\nThe automation hub bypasses GUI frameworks entirely — it speaks directly to the OS. This means it can control any application, not just those with APIs.`,
            usage: `# Example voice command:\n"Hey Nexaura, launch the Godot dev environment."\n\n# Internal execution chain:\n# 1. Gemini routes intent → os_automation plugin\n# 2. subprocess.Popen(['godot', '--editor'])\n# 3. pyautogui.hotkey('super', 'up')  # maximize\n# 4. pyautogui.moveTo(x, y, duration=0.3)\n# 5. pyautogui.click()\n\n# Screen mapping uses display resolution:\nimport pyautogui\nSW, SH = pyautogui.size()  # e.g., 1920x1080`,
            tags: ['PyAutoGUI', 'subprocess', 'System Interrupts', 'Template Matching', 'NLP Routing']
        },
        mobile: {
            icon: '[ NET ]', iconClass: 'fb-teal', title: 'Flask Mobile Remote Dashboard', sub: 'Feature · WSGI Network Control',
            desc: `A lightweight Flask WSGI server runs on a parallel background Werkzeug thread, binding to 0.0.0.0:5000. It exposes restricted RESTful API endpoints and serves a glassmorphic HTML/JS/CSS dashboard.\n\nThis allows any device on the same Wi-Fi subnet to monitor system state, view emotion readings, and trigger command executions — effectively bypassing the Porcupine voice layer for keyboard-based remote control.`,
            usage: `# Flask initializes automatically with main.py\n# Your terminal will log the bound IP:\n# [NET] WSGI Server active on http://192.168.1.105:5000nn# REST endpoint (POST):\nPOST /api/execute\nContent-Type: application/json\n{ "command": "open spotify and play lofi" }\n\n# CORS is locked to local subnet CIDR only.\n# Authentication: session token (configurable)\n\n# Access from any device on your Wi-Fi:\n# Open 192.168.1.105:5000 in any browser.`,
            tags: ['Flask', 'Werkzeug', 'REST API', 'CORS', 'Local Subnet', 'WSGI']
        },
        voice: {
            icon: '[ VOC ]', iconClass: 'fb-blue', title: 'ElevenLabs Neural Speech Synthesis', sub: 'Feature · Studio-Grade TTS',
            desc: `Nexaura bypasses legacy monotonic TTS engines (pyttsx3, SAPI5) entirely. Gemini's synthesized response strings are piped directly into the ElevenLabs neural API with programmatic control over stability bounds, similarity_boost percentages, and style scaling.\n\nAsync byte streaming decodes chunks as they arrive, feeding directly into the PyAudio playback buffer for ultra-low perceived latency. The voice adapts its parameters based on the current emotional context injected from DeepFace.`,
            usage: `# config.py\nELEVENLABS_API_KEY = "your_key_from_elevenlabs.io"\nVOICE_ID = "your_voice_uuid"\n\n# Voice parameters (tuned per emotion state)\nVOICE_SETTINGS = {\n    "stability": 0.5,        # 0.0 = expressive, 1.0 = stable\n    "similarity_boost": 0.75, # voice identity strength\n    "style": 0.0,            # 0.0 = neutral style\n    "use_speaker_boost": True\n}\n\n# Streaming begins on first LLM token received.\n# Audio plays back via PyAudio buffer.`,
            tags: ['ElevenLabs', 'Neural TTS', 'PyAudio', 'Async Streaming', 'Emotion-Adaptive']
        },
        security: {
            icon: '[ SEC ]', iconClass: 'fb-green', title: 'Air-Gapped Local Execution', sub: 'Feature · Data Sovereignty',
            desc: `Privacy is fundamental to Nexaura's architecture. Acoustic wake word modeling, facial CNN matrices, and SQLite memory graph operations are 100% sandboxed to local edge hardware.\n\nThe only authorized network egress events are: (1) sanitized NLP text to Gemini Pro API, and (2) TTS instruction strings to ElevenLabs. Zero raw sensor data — no audio bytes, no video frames, no biometric data — ever leaves your device.`,
            usage: `# Verify data sovereignty yourself:\n# 1. Open your OS firewall logs and monitor traffic.\n# 2. You will observe ZERO unauthorized egress packets.\n# 3. Only 2 external connections:\n#    → api.generativelanguage.googleapis.com (Gemini)\n#    → api.elevenlabs.io (TTS)\n\n# Inspect your memory vault directly:\nsqlite3 data/vault.db "SELECT * FROM interactions_log;"\n\n# Air-gap mode (Ollama fallback only):\n# Disable network, Nexaura routes to local Llama 3.`,
            tags: ['Zero Data Egress', 'Edge Compute', 'Air-Gap', 'Data Sovereignty', 'Local Inference']
        },
        local_llm: {
            icon: '[ LCL ]', iconClass: 'fb-purple', title: 'Ollama Local LLM Fallback', sub: 'Feature · Offline Inference',
            desc: `To guarantee 100% availability, Nexaura implements an automatic failover routing protocol. If Gemini Pro times out (configurable threshold, default 8 seconds) or the device goes offline, the Logic Engine seamlessly reroutes NLP payloads to a quantized local model running via the Ollama daemon.\n\nThis transition is invisible to the user — response quality may decrease slightly, but the system remains fully operational with zero interruption. Llama 3 8B (Q4_K_M quantization) is the recommended default fallback.`,
            usage: `# Step 1: Install Ollama\n# Visit https://ollama.com and install for your OS.\n\n# Step 2: Pull a quantized model\nollama pull llama3  # ~4.7GB download\n\n# Step 3: Enable in config.py\nFALLBACK_MODEL = "llama3"\nFALLBACK_TIMEOUT_SECONDS = 8\nENABLE_FALLBACK = True\n\n# Nexaura auto-manages the switch.\n# Test it by disabling network temporarily.\n# [SYS] Gemini timeout → routing to llama3 fallback`,
            tags: ['Ollama', 'Llama 3', 'Q4_K_M', 'Offline Mode', 'Automatic Failover']
        },
        stack_engine: {
            icon: '[ STK ]', iconClass: 'fb-amber', title: 'Python 3.11.9 — CPython Interpreter', sub: 'Stack · Core Engine',
            desc: `Nexaura targets Python 3.11 specifically for PEP 659 — the Specializing Adaptive Interpreter. This provides up to 60% faster execution for the intensive I/O-bound threading operations central to Nexaura's architecture.\n\nPython's GIL (Global Interpreter Lock) is bypassed for heavy OpenCV matrix calculations using multiprocessing libraries, while asyncio handles concurrent I/O operations across Flask, PyAudio, and the Gemini API client.`,
            usage: `# Verify you have the correct version\npython --version\n# Expected: Python 3.11.9\n\n# Execution model:\n# Core loop    → Main thread (GIL-bound)\n# Audio stream → Daemon thread (I/O-bound, fine with GIL)\n# Flask WSGI   → Daemon thread (I/O-bound)\n# OpenCV ops   → multiprocessing.Process (bypasses GIL)\n\n# Performance baseline:\n# Python 3.9:  ~220ms avg loop iteration\n# Python 3.11: ~140ms avg loop iteration (-36%)`,
            tags: ['Python 3.11.9', 'PEP 659', 'CPython', 'GIL', 'multiprocessing', 'asyncio']
        },
        stack_ai: {
            icon: '[ STK ]', iconClass: 'fb-blue', title: 'Gemini Pro — Multimodal LLM', sub: 'Stack · AI Brain',
            desc: `Gemini Pro processes deeply engineered context windows — not bare user queries. Each API call includes emotional state, historical context arrays, active plugin registry, and NLP intent classification.\n\nGeneration configs are strictly locked: temperature=0.2, response_mime_type="application/json". This forces Gemini to output parseable JSON dictionaries, not conversational text, enabling deterministic downstream OS automation without hallucinations.`,
            usage: `# Install the SDK\npip install google-generativeai\n\n# Initialize with locked generation config\nimport google.generativeai as genai\n\ngenai.configure(api_key=os.environ['GEMINI_API_KEY'])\n\nmodel = genai.GenerativeModel(\n    model_name='gemini-pro',\n    generation_config={\n        "temperature": 0.2,\n        "response_mime_type": "application/json"\n    }\n)`,
            tags: ['Gemini Pro', 'google-generativeai', 'JSON Mode', 'temperature=0.2', 'Context Engineering']
        },
        stack_vision: {
            icon: '[ STK ]', iconClass: 'fb-green', title: 'DeepFace — Emotion Analysis CNN', sub: 'Stack · Vision Layer',
            desc: `DeepFace is a lightweight abstraction layer over state-of-the-art CNNs — VGG-Face, Facenet, and OpenCV Haarcascades. In Nexaura it runs in non-blocking mode, sampling one frame every 10 seconds to compute logit arrays without stalling the primary event loop.\n\nenforce_detection=False ensures the analysis never throws an exception on a partially visible face, which is critical for a production system that must never crash.`,
            usage: `pip install deepface\n\nfrom deepface import DeepFace\nimport cv2\n\ncap = cv2.VideoCapture(0)\nret, frame = cap.read()\n\nresult = DeepFace.analyze(\n    frame,\n    enforce_detection=False,   # never crash on partial face\n    actions=['emotion'],       # only what we need\n    silent=True\n)\n\ndominant = result[0]['dominant_emotion']\n# e.g., 'happy', 'neutral', 'angry'`,
            tags: ['DeepFace', 'VGG-Face', 'Facenet', 'OpenCV', 'Non-blocking', 'enforce_detection=False']
        },
        stack_db: {
            icon: '[ STK ]', iconClass: 'fb-amber', title: 'SQLite3 — Async Memory Vault', sub: 'Stack · Persistence Layer',
            desc: `Nexaura uses SQLite3 with Write-Ahead Logging (WAL) to handle high-frequency memory ingestion from multiple concurrent threads. WAL allows simultaneous non-blocking reads and writes — critical when the audio thread, vision thread, and core loop all need to access the vault concurrently.\n\nData schema: interactions_log (timestamped NLP records), preference_weights (learned workflow biases), active_plugins (registered module registry). All Python dicts/lists are serialized as JSON blobs before committing.`,
            usage: `import sqlite3, json\n\nconn = sqlite3.connect('data/vault.db', check_same_thread=False)\nconn.execute("PRAGMA journal_mode=WAL")\n\n# Write an interaction\nconn.execute(\n    "INSERT INTO interactions_log (timestamp, query, response, emotion) VALUES (?,?,?,?)",\n    (time.time(), json.dumps(query), json.dumps(response), emotion)\n)\nconn.commit()\n\n# Read last 5 interactions for context injection\nrows = conn.execute(\n    "SELECT * FROM interactions_log ORDER BY timestamp DESC LIMIT 5"\n).fetchall()`,
            tags: ['SQLite3', 'WAL Mode', 'JSON Blobs', 'Concurrent Access', 'LRU Context']
        },
        stack_ui: {
            icon: '[ STK ]', iconClass: 'fb-purple', title: 'PyQt6 — Desktop GUI Layer', sub: 'Stack · Visual Interface',
            desc: `PyQt6 binds directly to Qt's C++ rendering pipeline, enabling GPU-accelerated, transparent overlay windows on top of the host OS workspace. Frameless, always-on-top widgets display real-time mic waveforms and system state without obscuring the workspace.\n\nCross-thread communication uses Qt Signals and Slots — the only thread-safe way to update visual elements from background daemon threads in Python.`,
            usage: `pip install PyQt6\n\nfrom PyQt6.QtWidgets import QApplication, QWidget\nfrom PyQt6.QtCore import Qt\n\nclass NexauraOverlay(QWidget):\n    def __init__(self):\n        super().__init__()\n        # Frameless, transparent, always-on-top\n        self.setWindowFlags(\n            Qt.WindowType.FramelessWindowHint |\n            Qt.WindowType.WindowStaysOnTopHint\n        )\n        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)`,
            tags: ['PyQt6', 'Qt C++', 'Frameless Window', 'GPU Rendering', 'Signals & Slots']
        },
        stack_net: {
            icon: '[ STK ]', iconClass: 'fb-teal', title: 'Flask + Werkzeug — Mobile WSGI', sub: 'Stack · Network Layer',
            desc: `Flask runs on a background Werkzeug thread, strictly separated from the core engine loop. Binding to 0.0.0.0 exposes the REST API to the full local subnet. CORS is locked to the local CIDR range (192.168.x.x) only — no public internet exposure.\n\nHTTP POST payloads received at /api/execute are queued and flushed into the main OS action parser, maintaining a clean separation between the network layer and the automation layer.`,
            usage: `pip install flask\n\nfrom flask import Flask, request, jsonify\nfrom flask_cors import CORS\n\napp = Flask(__name__)\nCORS(app, origins=['192.168.*.*'])\n\n@app.route('/api/execute', methods=['POST'])\ndef execute():\n    payload = request.get_json()\n    command = payload.get('command')\n    action_queue.put(command)  # thread-safe queue\n    return jsonify({"status": "queued", "command": command})\n\n# Run on daemon thread\nthreading.Thread(\n    target=lambda: app.run(host='0.0.0.0', port=5000),\n    daemon=True\n).start()`,
            tags: ['Flask', 'Werkzeug', 'REST API', 'CORS', '0.0.0.0', 'Thread-safe Queue']
        },
        stack_sr: {
            icon: '[ STK ]', iconClass: 'fb-purple', title: 'SpeechRecognition API', sub: 'Stack · Audio Layer',
            desc: `The speech_recognition library serves as the core acoustic conversion layer. It listens to the user's voice input and translates it into parseable text commands.`,
            usage: `import speech_recognition as sr\n\nr = sr.Recognizer()\nwith sr.Microphone() as source:\n    audio = r.listen(source)\n    text = r.recognize_google(audio)`,
            tags: ['SpeechRecognition', 'Audio Processing', 'Voice-to-Text']
        },
        stack_tts: {
            icon: '[ STK ]', iconClass: 'fb-blue', title: 'pyttsx3 Offline TTS', sub: 'Stack · Speech Synthesis',
            desc: `pyttsx3 is an offline text-to-speech conversion library in Python. It provides reliable voice output without requiring internet access or external API calls, ensuring high availability.`,
            usage: `import pyttsx3\n\nengine = pyttsx3.init()\nengine.say("Nexaura systems online.")\nengine.runAndWait()`,
            tags: ['pyttsx3', 'Offline TTS', 'Speech Synthesis']
        },
        stack_env: {
            icon: '[ STK ]', iconClass: 'fb-green', title: 'python-dotenv', sub: 'Stack · Security',
            desc: `python-dotenv reads key-value pairs from a .env file and sets them as environment variables. This keeps sensitive API keys secure and out of the main source code repository.`,
            usage: `from dotenv import load_dotenv\nimport os\n\nload_dotenv()\nAPI_KEY = os.getenv("GEMINI_API_KEY")`,
            tags: ['Security', 'Environment Variables', 'Dotenv']
        },
        
        /* ─── NEW STACK MODULES ADDED HERE ─── */
        stack_webbrowser: {
            icon: '[ WWW ]', iconClass: 'fb-teal', title: 'webbrowser Module', sub: 'Stack · Web Automation',
            desc: `The built-in webbrowser module allows Nexaura to interface directly with the default system browser to open URLs, perform web searches, and navigate online resources automatically based on voice commands.`,
            usage: `import webbrowser\n\n# Nexaura automating a browser launch\nwebbrowser.open("https://github.com/Sam-Dev-161127")`,
            tags: ['webbrowser', 'Automation', 'Python Standard Library']
        },
        stack_requests: {
            icon: '[ NET ]', iconClass: 'fb-amber', title: 'Requests Library', sub: 'Stack · Data Fetching',
            desc: `Requests is an elegant and simple HTTP library for Python. Nexaura uses it to fetch real-time information from the web, interact with REST APIs, and download required online data seamlessly without manual interaction.`,
            usage: `import requests\n\n# Nexaura fetching real-time data\nresponse = requests.get("https://api.github.com")\nif response.status_code == 200:\n    data = response.json()`,
            tags: ['requests', 'HTTP', 'API', 'Data Fetching']
        },
        stack_os: {
            icon: '[ SYS ]', iconClass: 'fb-red', title: 'os Module', sub: 'Stack · System Control',
            desc: `The os module provides a portable way of using operating system dependent functionality. Nexaura relies on it to launch desktop applications (like VS Code or Notepad), manage files, and execute core system commands.`,
            usage: `import os\n\n# Nexaura launching a desktop application (Windows)\nos.system("notepad.exe")\n\n# Or reading environment details\nuser_path = os.getenv('USERPROFILE')`,
            tags: ['os', 'System Control', 'App Launching', 'File Management']
        }
        /* ─── END OF NEW MODAL DATA ─── */
    };

    const modal = document.getElementById('featureModal');
    
    function openModal(id) {
        const d = modalData[id];
        if(!d) return;
        
        document.getElementById('m-icon').textContent = d.icon;
        document.getElementById('m-icon').className = 'feat-badge ' + (d.iconClass || 'fb-blue');
        document.getElementById('m-title').textContent = d.title;
        document.getElementById('m-sub').textContent = d.sub;
        document.getElementById('m-desc').textContent = d.desc;
        document.getElementById('m-usage').textContent = d.usage;
        
        const tagsEl = document.getElementById('m-tags');
        tagsEl.innerHTML = (d.tags || []).map(t => `<span class="modal-tag">${t}</span>`).join('');
        
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    modal.addEventListener('click', e => { 
        if (e.target === modal) closeModal(); 
    });

    document.addEventListener('keydown', e => { 
        if (e.key === 'Escape') closeModal(); 
    });

</script>
</body>
</html>