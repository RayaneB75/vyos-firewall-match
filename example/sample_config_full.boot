firewall {
    group {
        interface-group VRF-RESEL-AP {
            interface "eth2"
        }
        interface-group VRF-RESEL-DMZ {
            interface "eth3"
        }
        interface-group VRF-RESEL-MAIN {
            interface "eth1"
        }
        interface-group VRF-RESEL-PUBLIC {
            interface "eth4"
        }
        interface-group VRF-RESEL-SYSTEM {
            interface "eth5"
        }
        interface-group VRF-RESEL-USER-1 {
            interface "eth6"
        }
        network-group NG-DEFAULT-V4 {
            network "0.0.0.0/0"
        }
        ipv6-network-group NG-DEFAULT-V6 {
            network "::/0"
        }
        ipv6-network-group NG-RESEL-SUPERNET-V6 {
            network "2a00:5881:3000::/40"
        }
        network-group PFX-RESEL-V4 {
            network "10.32.0.0/16"
            network "10.33.0.0/16"
            network "10.34.0.0/16"
            network "10.35.0.0/16"
            network "10.36.0.0/16"
            network "10.37.0.0/16"
            network "10.38.0.0/16"
        }
        network-group PFX-RESEL-DMZ-V4 {
            network "10.4.0.0/16"
            network "10.36.0.0/16"
            network "10.68.0.0/16"
        }
        network-group PFX-RESEL-ADMINS-V4 {
            network "10.2.0.0/23"
            network "10.36.0.0/23"
            network "10.68.0.0/23"
        }
        network-group PFX-RESEL-CAPTIVE-REDIRECT-V4 {
            network "10.4.13.6/32"
            network "10.36.13.6/32"
            network "10.70.13.6/32"
        }
        network-group PFX-RESEL-DHCP-V4 {
            network "10.3.14.1/32"
            network "10.3.14.101/32"
            network "10.35.14.1/32"
            network "10.67.14.1/32"
        }
        network-group PFX-RESEL-DMZ-RP-V4 {
            network "10.4.9.1/32"
            network "10.4.9.2/32"
            network "89.234.162.251/32"
        }
        network-group PFX-RESEL-DNS-V4 {
            network "10.4.13.2/32"
            network "10.4.13.102/32"
            network "10.36.13.2/32"
            network "10.68.13.2/32"
        }
        network-group PFX-RESEL-JUMPS-V4 {
            network "10.2.255.1/32"
            network "10.34.255.1/32"
            network "10.67.255.1/32"
        }
        network-group PFX-RESEL-MAIL-V4 {
            network "10.4.6.11/32"
            network "10.36.6.11/32"
        }
        network-group PFX-RESEL-RADIUS-V4 {
            network "10.3.12.1/32"
            network "10.3.12.101/32"
            network "10.35.12.1/32"
            network "10.67.12.1/32"
        }
        network-group PFX-RESEL-REGISTRATION-DNS-V4 {
            network "10.4.13.5/32"
            network "10.36.13.5/32"
            network "10.70.13.5/32"
        }
        network-group PFX-RESEL-SIEM-V4 {
            network "10.2.22.0/24"
            network "10.34.22.0/24"
            network "10.66.22.0/24"
        }
        network-group PFX-RESEL-SYSTEM-V4 {
            network "10.0.0.0/23"
            network "10.32.0.0/23"
            network "10.64.0.0/23"
        }
        network-group PFX-RESEL-USER-2751-V4 {
            network "10.48.4.0/23"
        }
        network-group PFX-RESEL-USER-2752-V4 {
            network "10.48.8.0/23"
        }
        network-group PFX-RESEL-USER-2753-V4 {
            network "10.48.12.0/23"
        }
        network-group PFX-RESEL-USER-2754-V4 {
            network "10.48.16.0/23"
        }
        network-group PFX-RESEL-USER-2755-V4 {
            network "10.48.20.0/23"
        }
        network-group PFX-RESEL-USER-2756-V4 {
            network "10.48.24.0/23"
        }
        network-group PFX-RESEL-USER-2757-V4 {
            network "10.48.28.0/23"
        }
        network-group PFX-RESEL-USER-2758-V4 {
            network "10.48.32.0/23"
        }
        network-group PFX-RESEL-USER-2759-V4 {
            network "10.48.36.0/23"
        }
        network-group PFX-RESEL-USER-2760-V4 {
            network "10.48.40.0/23"
        }
        network-group PFX-RESEL-USER-2761-V4 {
            network "10.48.44.0/23"
        }
        network-group PFX-RESEL-USER-2762-V4 {
            network "10.48.48.0/23"
        }
        network-group PFX-RESEL-USER-2763-V4 {
            network "10.48.52.0/23"
        }
        network-group PFX-RESEL-USER-2764-V4 {
            network "10.48.56.0/23"
        }
        network-group PFX-RESEL-USER-2765-V4 {
            network "10.48.60.0/23"
        }
        network-group PFX-RESEL-USER-2766-V4 {
            network "10.48.64.0/23"
        }
        network-group PFX-RESEL-USER-2767-V4 {
            network "10.48.68.0/23"
        }
        network-group PFX-RESEL-USER-2768-V4 {
            network "10.48.72.0/23"
        }
        network-group PFX-RESEL-USER-2769-V4 {
            network "10.48.76.0/23"
        }
        network-group PFX-RESEL-USER-2770-V4 {
            network "10.48.80.0/23"
        }
        network-group PFX-RESEL-USER-2771-V4 {
            network "10.48.84.0/23"
        }
        network-group PFX-RESEL-USER-2772-V4 {
            network "10.48.88.0/23"
        }
        network-group PFX-RESEL-USER-2773-V4 {
            network "10.48.92.0/23"
        }
        network-group PFX-RESEL-USER-2774-V4 {
            network "10.48.96.0/23"
        }
        network-group PFX-RESEL-USER-2775-V4 {
            network "10.48.100.0/23"
        }
        network-group PFX-RESEL-USER-2776-V4 {
            network "10.48.104.0/23"
        }
        network-group PFX-RESEL-USER-2777-V4 {
            network "10.48.108.0/23"
        }
        network-group PFX-RESEL-USER-2778-V4 {
            network "10.48.112.0/23"
        }
        network-group PFX-RESEL-USER-2779-V4 {
            network "10.48.116.0/23"
        }
        network-group PFX-RESEL-USER-2780-V4 {
            network "10.48.120.0/23"
        }
        network-group PFX-RESEL-USER-2781-V4 {
            network "10.48.124.0/23"
        }
        network-group PFX-RESEL-USER-2782-V4 {
            network "10.48.128.0/23"
        }
        network-group PFX-RESEL-USER-2783-V4 {
            network "10.48.132.0/23"
        }
        network-group PFX-RESEL-USER-2784-V4 {
            network "10.48.136.0/23"
        }
        network-group PFX-RESEL-USER-2785-V4 {
            network "10.48.140.0/23"
        }
        network-group PFX-RESEL-USER-2786-V4 {
            network "10.48.144.0/23"
        }
        network-group PFX-RESEL-USER-2787-V4 {
            network "10.48.148.0/23"
        }
        network-group PFX-RESEL-USER-2788-V4 {
            network "10.48.152.0/23"
        }
        network-group PFX-RESEL-USER-2789-V4 {
            network "10.48.156.0/23"
        }
        network-group PFX-RESEL-USER-2790-V4 {
            network "10.48.160.0/23"
        }
        network-group PFX-RESEL-USER-2791-V4 {
            network "10.48.164.0/23"
        }
        network-group PFX-RESEL-USER-2792-V4 {
            network "10.48.168.0/23"
        }
        network-group PFX-RESEL-USER-2793-V4 {
            network "10.48.172.0/23"
        }
        network-group PFX-RESEL-USER-2794-V4 {
            network "10.48.176.0/23"
        }
        network-group PFX-RESEL-USER-2795-V4 {
            network "10.48.180.0/23"
        }
        network-group PFX-RESEL-USER-2796-V4 {
            network "10.48.184.0/23"
        }
        network-group PFX-RESEL-USER-2797-V4 {
            network "10.48.188.0/23"
        }
        network-group PFX-RESEL-USER-2798-V4 {
            network "10.48.192.0/23"
        }
        network-group PFX-RESEL-USER-2799-V4 {
            network "10.48.196.0/23"
        }
        network-group PFX-RESEL-USER-2800-V4 {
            network "10.48.200.0/23"
        }
        network-group PFX-RESEL-USER-2801-V4 {
            network "10.48.204.0/23"
        }
        network-group PFX-RESEL-USER-2802-V4 {
            network "10.48.208.0/23"
        }
        network-group PFX-RESEL-USER-2803-V4 {
            network "10.48.212.0/23"
        }
        network-group PFX-RESEL-USER-2804-V4 {
            network "10.48.216.0/23"
        }
        network-group PFX-RESEL-USER-2805-V4 {
            network "10.48.220.0/23"
        }
        network-group PFX-RESEL-USER-2806-V4 {
            network "10.48.224.0/23"
        }
        network-group PFX-RESEL-USER-2807-V4 {
            network "10.48.228.0/23"
        }
        network-group PFX-RESEL-USER-2808-V4 {
            network "10.48.232.0/23"
        }
        network-group PFX-RESEL-USER-2809-V4 {
            network "10.48.236.0/23"
        }
        network-group PFX-RESEL-USER-2810-V4 {
            network "10.48.240.0/23"
        }
        network-group PFX-RESEL-USER-2811-V4 {
            network "10.48.244.0/23"
        }
        network-group PFX-RESEL-USER-2812-V4 {
            network "10.48.248.0/23"
        }
        network-group PFX-RESEL-USER-2813-V4 {
            network "10.48.252.0/23"
        }
        network-group PFX-RESEL-USER-2814-V4 {
            network "10.49.0.0/23"
        }
        network-group PFX-RESEL-USER-2815-V4 {
            network "10.49.4.0/23"
        }
        network-group PFX-RESEL-USER-2816-V4 {
            network "10.49.8.0/23"
        }
        network-group PFX-RESEL-USER-2817-V4 {
            network "10.49.12.0/23"
        }
        network-group PFX-RESEL-USER-2818-V4 {
            network "10.49.16.0/23"
        }
        network-group PFX-RESEL-USER-2819-V4 {
            network "10.49.20.0/23"
        }
        network-group PFX-RESEL-USER-2820-V4 {
            network "10.49.24.0/23"
        }
        network-group PFX-RESEL-USER-2821-V4 {
            network "10.49.28.0/23"
        }
        network-group PFX-RESEL-USER-2822-V4 {
            network "10.49.32.0/23"
        }
        network-group PFX-RESEL-USER-2823-V4 {
            network "10.49.36.0/23"
        }
        network-group PFX-RESEL-USER-2824-V4 {
            network "10.49.40.0/23"
        }
        network-group PFX-RESEL-USER-2825-V4 {
            network "10.49.44.0/23"
        }
        network-group PFX-RESEL-USER-2826-V4 {
            network "10.49.48.0/23"
        }
        network-group PFX-RESEL-USER-2827-V4 {
            network "10.49.52.0/23"
        }
        network-group PFX-RESEL-USER-2828-V4 {
            network "10.49.56.0/23"
        }
        network-group PFX-RESEL-USER-2829-V4 {
            network "10.49.60.0/23"
        }
        network-group PFX-RESEL-USER-2830-V4 {
            network "10.49.64.0/23"
        }
        network-group PFX-RESEL-USER-2831-V4 {
            network "10.49.68.0/23"
        }
        network-group PFX-RESEL-USER-2832-V4 {
            network "10.49.72.0/23"
        }
        network-group PFX-RESEL-USER-2833-V4 {
            network "10.49.76.0/23"
        }
        network-group PFX-RESEL-USER-2834-V4 {
            network "10.49.80.0/23"
        }
        network-group PFX-RESEL-USER-2835-V4 {
            network "10.49.84.0/23"
        }
        network-group PFX-RESEL-USER-2836-V4 {
            network "10.49.88.0/23"
        }
        network-group PFX-RESEL-USER-2837-V4 {
            network "10.49.92.0/23"
        }
        network-group PFX-RESEL-USER-2838-V4 {
            network "10.49.96.0/23"
        }
        network-group PFX-RESEL-USER-2839-V4 {
            network "10.49.100.0/23"
        }
        network-group PFX-RESEL-USER-2840-V4 {
            network "10.49.104.0/23"
        }
        network-group PFX-RESEL-USER-2841-V4 {
            network "10.49.108.0/23"
        }
        network-group PFX-RESEL-USER-2842-V4 {
            network "10.49.112.0/23"
        }
        network-group PFX-RESEL-USER-2843-V4 {
            network "10.49.116.0/23"
        }
        network-group PFX-RESEL-USER-2844-V4 {
            network "10.49.120.0/23"
        }
        network-group PFX-RESEL-USER-2845-V4 {
            network "10.49.124.0/23"
        }
        network-group PFX-RESEL-USER-2846-V4 {
            network "10.49.128.0/23"
        }
        network-group PFX-RESEL-USER-2847-V4 {
            network "10.49.132.0/23"
        }
        network-group PFX-RESEL-USER-2848-V4 {
            network "10.49.136.0/23"
        }
        network-group PFX-RESEL-USER-2849-V4 {
            network "10.49.140.0/23"
        }
        network-group PFX-RESEL-USER-2850-V4 {
            network "10.49.144.0/23"
        }
        network-group PFX-RESEL-USER-2851-V4 {
            network "10.49.148.0/23"
        }
        network-group PFX-RESEL-USER-2852-V4 {
            network "10.49.152.0/23"
        }
        network-group PFX-RESEL-USER-2853-V4 {
            network "10.49.156.0/23"
        }
        network-group PFX-RESEL-USER-2854-V4 {
            network "10.49.160.0/23"
        }
        network-group PFX-RESEL-USER-2855-V4 {
            network "10.49.164.0/23"
        }
        network-group PFX-RESEL-USER-2856-V4 {
            network "10.49.168.0/23"
        }
        network-group PFX-RESEL-USER-2857-V4 {
            network "10.49.172.0/23"
        }
        network-group PFX-RESEL-USER-2858-V4 {
            network "10.49.176.0/23"
        }
        network-group PFX-RESEL-USER-2859-V4 {
            network "10.49.180.0/23"
        }
        network-group PFX-RESEL-USER-2860-V4 {
            network "10.49.184.0/23"
        }
        network-group PFX-RESEL-USER-2861-V4 {
            network "10.49.188.0/23"
        }
        network-group PFX-RESEL-USER-2862-V4 {
            network "10.49.192.0/23"
        }
        network-group PFX-RESEL-USER-2863-V4 {
            network "10.49.196.0/23"
        }
        network-group PFX-RESEL-USER-2864-V4 {
            network "10.49.200.0/23"
        }
        network-group PFX-RESEL-USER-2865-V4 {
            network "10.49.204.0/23"
        }
        network-group PFX-RESEL-USER-2866-V4 {
            network "10.49.208.0/23"
        }
        network-group PFX-RESEL-USER-2867-V4 {
            network "10.49.212.0/23"
        }
        network-group PFX-RESEL-USER-2868-V4 {
            network "10.49.216.0/23"
        }
        network-group PFX-RESEL-USER-2869-V4 {
            network "10.49.220.0/23"
        }
        network-group PFX-RESEL-USER-2870-V4 {
            network "10.49.224.0/23"
        }
        network-group PFX-RESEL-USER-2871-V4 {
            network "10.49.228.0/23"
        }
        network-group PFX-RESEL-USER-2872-V4 {
            network "10.49.232.0/23"
        }
        network-group PFX-RESEL-USER-2873-V4 {
            network "10.49.236.0/23"
        }
        network-group PFX-RESEL-USER-2874-V4 {
            network "10.49.240.0/23"
        }
        network-group PFX-RESEL-USER-2875-V4 {
            network "10.49.244.0/23"
        }
        network-group PFX-RESEL-USER-2876-V4 {
            network "10.49.248.0/23"
        }
        network-group PFX-RESEL-USER-2877-V4 {
            network "10.49.252.0/23"
        }
        network-group PFX-RESEL-USER-2878-V4 {
            network "10.50.0.0/23"
        }
        network-group PFX-RESEL-USER-2879-V4 {
            network "10.50.4.0/23"
        }
        network-group PFX-RESEL-USER-2880-V4 {
            network "10.50.8.0/23"
        }
        network-group PFX-RESEL-USER-2881-V4 {
            network "10.50.12.0/23"
        }
        network-group PFX-RESEL-USER-2882-V4 {
            network "10.50.16.0/23"
        }
        network-group PFX-RESEL-USER-2883-V4 {
            network "10.50.20.0/23"
        }
        network-group PFX-RESEL-USER-2884-V4 {
            network "10.50.24.0/23"
        }
        network-group PFX-RESEL-USER-2885-V4 {
            network "10.50.28.0/23"
        }
        network-group PFX-RESEL-USER-2886-V4 {
            network "10.50.32.0/23"
        }
        network-group PFX-RESEL-USER-2887-V4 {
            network "10.50.36.0/23"
        }
        network-group PFX-RESEL-USER-2888-V4 {
            network "10.50.40.0/23"
        }
        network-group PFX-RESEL-USER-2889-V4 {
            network "10.50.44.0/23"
        }
        network-group PFX-RESEL-USER-2890-V4 {
            network "10.50.48.0/23"
        }
        network-group PFX-RESEL-USER-2891-V4 {
            network "10.50.52.0/23"
        }
        network-group PFX-RESEL-USER-2892-V4 {
            network "10.50.56.0/23"
        }
        network-group PFX-RESEL-USER-2893-V4 {
            network "10.50.60.0/23"
        }
        network-group PFX-RESEL-USER-2894-V4 {
            network "10.50.64.0/23"
        }
        network-group PFX-RESEL-USER-2895-V4 {
            network "10.50.68.0/23"
        }
        network-group PFX-RESEL-USER-2896-V4 {
            network "10.50.72.0/23"
        }
        network-group PFX-RESEL-USER-2897-V4 {
            network "10.50.76.0/23"
        }
        network-group PFX-RESEL-USER-2898-V4 {
            network "10.50.80.0/23"
        }
        network-group PFX-RESEL-USER-2899-V4 {
            network "10.50.84.0/23"
        }
        network-group PFX-RESEL-USER-2900-V4 {
            network "10.50.88.0/23"
        }
        network-group PFX-RESEL-USER-2901-V4 {
            network "10.50.92.0/23"
        }
        network-group PFX-RESEL-USER-2902-V4 {
            network "10.50.96.0/23"
        }
        network-group PFX-RESEL-USER-2903-V4 {
            network "10.50.100.0/23"
        }
        network-group PFX-RESEL-USER-2904-V4 {
            network "10.50.104.0/23"
        }
        network-group PFX-RESEL-USER-2905-V4 {
            network "10.50.108.0/23"
        }
        network-group PFX-RESEL-USER-2906-V4 {
            network "10.50.112.0/23"
        }
        network-group PFX-RESEL-USER-2907-V4 {
            network "10.50.116.0/23"
        }
        network-group PFX-RESEL-USER-2908-V4 {
            network "10.50.120.0/23"
        }
        network-group PFX-RESEL-USER-2909-V4 {
            network "10.50.124.0/23"
        }
        network-group PFX-RESEL-USER-2910-V4 {
            network "10.50.128.0/23"
        }
        network-group PFX-RESEL-USER-2911-V4 {
            network "10.50.132.0/23"
        }
        network-group PFX-RESEL-USER-2912-V4 {
            network "10.50.136.0/23"
        }
        network-group PFX-RESEL-USER-2913-V4 {
            network "10.50.140.0/23"
        }
        network-group PFX-RESEL-USER-2914-V4 {
            network "10.50.144.0/23"
        }
        network-group PFX-RESEL-USER-2915-V4 {
            network "10.50.148.0/23"
        }
        network-group PFX-RESEL-USER-2916-V4 {
            network "10.50.152.0/23"
        }
        network-group PFX-RESEL-USER-2917-V4 {
            network "10.50.156.0/23"
        }
        network-group PFX-RESEL-USER-2918-V4 {
            network "10.50.160.0/23"
        }
        network-group PFX-RESEL-USER-2919-V4 {
            network "10.50.164.0/23"
        }
        network-group PFX-RESEL-USER-2920-V4 {
            network "10.50.168.0/23"
        }
        network-group PFX-RESEL-USER-2921-V4 {
            network "10.50.172.0/23"
        }
        network-group PFX-RESEL-USER-2922-V4 {
            network "10.50.176.0/23"
        }
        network-group PFX-RESEL-USER-2923-V4 {
            network "10.50.180.0/23"
        }
        network-group PFX-RESEL-USER-2924-V4 {
            network "10.50.184.0/23"
        }
        network-group PFX-RESEL-USER-2925-V4 {
            network "10.50.188.0/23"
        }
        network-group PFX-RESEL-USER-2926-V4 {
            network "10.50.192.0/23"
        }
        network-group PFX-RESEL-USER-2927-V4 {
            network "10.50.196.0/23"
        }
        network-group PFX-RESEL-USER-2928-V4 {
            network "10.50.200.0/23"
        }
        network-group PFX-RESEL-USER-2929-V4 {
            network "10.50.204.0/23"
        }
        network-group PFX-RESEL-USER-2930-V4 {
            network "10.50.208.0/23"
        }
        network-group PFX-RESEL-USER-2931-V4 {
            network "10.50.212.0/23"
        }
        network-group PFX-RESEL-USER-2932-V4 {
            network "10.50.216.0/23"
        }
        network-group PFX-RESEL-USER-2933-V4 {
            network "10.50.220.0/23"
        }
        network-group PFX-RESEL-USER-2934-V4 {
            network "10.50.224.0/23"
        }
        network-group PFX-RESEL-USER-2935-V4 {
            network "10.50.228.0/23"
        }
        network-group PFX-RESEL-USER-2936-V4 {
            network "10.50.232.0/23"
        }
        network-group PFX-RESEL-USER-2937-V4 {
            network "10.50.236.0/23"
        }
        network-group PFX-RESEL-USER-2938-V4 {
            network "10.50.240.0/23"
        }
        network-group PFX-RESEL-USER-2939-V4 {
            network "10.50.244.0/23"
        }
        network-group PFX-RESEL-USER-2940-V4 {
            network "10.50.248.0/23"
        }
        network-group PFX-RESEL-USER-2941-V4 {
            network "10.50.252.0/23"
        }
        network-group PFX-RESEL-USER-2942-V4 {
            network "10.51.0.0/23"
        }
        network-group PFX-RESEL-USER-2943-V4 {
            network "10.51.4.0/23"
        }
        network-group PFX-RESEL-USER-2944-V4 {
            network "10.51.8.0/23"
        }
        network-group PFX-RESEL-USER-2945-V4 {
            network "10.51.12.0/23"
        }
        network-group PFX-RESEL-USER-2946-V4 {
            network "10.51.16.0/23"
        }
        network-group PFX-RESEL-USER-2947-V4 {
            network "10.51.20.0/23"
        }
        network-group PFX-RESEL-USER-2948-V4 {
            network "10.51.24.0/23"
        }
        network-group PFX-RESEL-USER-2949-V4 {
            network "10.51.28.0/23"
        }
        network-group PFX-RESEL-USER-2950-V4 {
            network "10.51.32.0/23"
        }
        network-group PFX-RESEL-USER-2951-V4 {
            network "10.51.36.0/23"
        }
        network-group PFX-RESEL-USER-2952-V4 {
            network "10.51.40.0/23"
        }
        network-group PFX-RESEL-USER-2953-V4 {
            network "10.51.44.0/23"
        }
        network-group PFX-RESEL-USER-2954-V4 {
            network "10.51.48.0/23"
        }
        network-group PFX-RESEL-USER-2955-V4 {
            network "10.51.52.0/23"
        }
        network-group PFX-RESEL-USER-2956-V4 {
            network "10.51.56.0/23"
        }
        network-group PFX-RESEL-USER-2957-V4 {
            network "10.51.60.0/23"
        }
        network-group PFX-RESEL-USER-2958-V4 {
            network "10.51.64.0/23"
        }
        network-group PFX-RESEL-USER-2959-V4 {
            network "10.51.68.0/23"
        }
        network-group PFX-RESEL-USER-2960-V4 {
            network "10.51.72.0/23"
        }
        network-group PFX-RESEL-USER-2961-V4 {
            network "10.51.76.0/23"
        }
        network-group PFX-RESEL-USER-2962-V4 {
            network "10.51.80.0/23"
        }
        network-group PFX-RESEL-USER-2963-V4 {
            network "10.51.84.0/23"
        }
        network-group PFX-RESEL-USER-2964-V4 {
            network "10.51.88.0/23"
        }
        network-group PFX-RESEL-USER-2965-V4 {
            network "10.51.92.0/23"
        }
        network-group PFX-RESEL-USER-2966-V4 {
            network "10.51.96.0/23"
        }
        network-group PFX-RESEL-USER-2967-V4 {
            network "10.51.100.0/23"
        }
        network-group PFX-RESEL-USER-2968-V4 {
            network "10.51.104.0/23"
        }
        network-group PFX-RESEL-USER-2969-V4 {
            network "10.51.108.0/23"
        }
        network-group PFX-RESEL-USER-2970-V4 {
            network "10.51.112.0/23"
        }
        network-group PFX-RESEL-USER-2971-V4 {
            network "10.51.116.0/23"
        }
        network-group PFX-RESEL-USER-2972-V4 {
            network "10.51.120.0/23"
        }
        network-group PFX-RESEL-USER-2973-V4 {
            network "10.51.124.0/23"
        }
        network-group PFX-RESEL-USER-2974-V4 {
            network "10.51.128.0/23"
        }
        network-group PFX-RESEL-USER-2975-V4 {
            network "10.51.132.0/23"
        }
        network-group PFX-RESEL-USER-2976-V4 {
            network "10.51.136.0/23"
        }
        network-group PFX-RESEL-USER-2977-V4 {
            network "10.51.140.0/23"
        }
        network-group PFX-RESEL-USER-2978-V4 {
            network "10.51.144.0/23"
        }
        network-group PFX-RESEL-USER-2979-V4 {
            network "10.51.148.0/23"
        }
        network-group PFX-RESEL-USER-2980-V4 {
            network "10.51.152.0/23"
        }
        network-group PFX-RESEL-USER-2981-V4 {
            network "10.51.156.0/23"
        }
        network-group PFX-RESEL-USER-2982-V4 {
            network "10.51.160.0/23"
        }
        network-group PFX-RESEL-USER-2983-V4 {
            network "10.51.164.0/23"
        }
        network-group PFX-RESEL-USER-2984-V4 {
            network "10.51.168.0/23"
        }
        network-group PFX-RESEL-USER-2985-V4 {
            network "10.51.172.0/23"
        }
        network-group PFX-RESEL-USER-2986-V4 {
            network "10.51.176.0/23"
        }
        network-group PFX-RESEL-USER-2987-V4 {
            network "10.51.180.0/23"
        }
        network-group PFX-RESEL-USER-2988-V4 {
            network "10.51.184.0/23"
        }
        network-group PFX-RESEL-USER-2989-V4 {
            network "10.51.188.0/23"
        }
        network-group PFX-RESEL-USER-2990-V4 {
            network "10.51.192.0/23"
        }
        network-group PFX-RESEL-USER-2991-V4 {
            network "10.51.196.0/23"
        }
        network-group PFX-RESEL-USER-2992-V4 {
            network "10.51.200.0/23"
        }
        network-group PFX-RESEL-USER-2993-V4 {
            network "10.51.204.0/23"
        }
        network-group PFX-RESEL-USER-2994-V4 {
            network "10.51.208.0/23"
        }
        network-group PFX-RESEL-USER-2995-V4 {
            network "10.51.212.0/23"
        }
        network-group PFX-RESEL-USER-CAPTIVE-V4 {
            network "10.38.0.0/16"
        }
        network-group PFX-RESEL-USER-BDE-V4 {
            network "10.39.128.0/17"
        }
        network-group PFX-RESEL-USER-UNKNOWN-V4 {
            network "10.48.0.0/23"
        }
        network-group PFX-RESEL-V4 {
            network "10.32.0.0/16"
            network "10.33.0.0/16"
            network "10.34.0.0/16"
            network "10.35.0.0/16"
            network "10.36.0.0/16"
            network "10.37.0.0/16"
            network "10.38.0.0/16"
        }
    }
    ipv4 {
        forward {
            /* naming convention is the following :
            
            (IP version) [ACTION] - SOURCE to DESTINATION - SERVICE
            
            */
            filter {
                default-log
                /* Captive portal rules */
                rule 10 {
                    action accept
                    description "(IPv4) [ACCEPT] - ESTABLISHED CONNECTIONS"
                    state "established"
                    state "related"
                }
                rule 20 {
                    action accept
                    description "(IPv4) [ACCEPT] - CAPTIVE to DMZ - resel.fr"
                    destination {
                        fqdn "resel.fr"
                        port http,https
                    }
                    inbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                    source {
                        group {
                            network-group PFX-RESEL-USER-CAPTIVE-V4
                        }
                    }
                    protocol tcp_udp
                }
                rule 30 {
                    action accept
                    description "(IPv4) [ACCEPT] - CAPTIVE to DMZ - DNS"
                    destination {
                        group {
                            network-group PFX-RESEL-REGISTRATION-DNS-V4
                        }
                        port 53
                    }
                    inbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                    protocol tcp_udp
                }
                rule 40 {
                    action accept
                    description "(IPv4) [ACCEPT] - CAPTIVE to DMZ - Redirect"
                    destination {
                        group {
                            network-group PFX-RESEL-CAPTIVE-REDIRECT-V4
                        }
                        port http,https
                    }
                    inbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                    protocol tcp_udp
                }
                rule 50 {
                    action accept
                    description "(IPv4) [ACCEPT] - CAPTIVE to SYSTEM - DHCP"
                    destination {
                        group {
                            network-group PFX-RESEL-DHCP-V4
                        }
                        port 67
                    }
                    inbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                    source {
                        group {
                            network-group PFX-RESEL-USER-CAPTIVE-V4
                        }
                    }
                    protocol udp
                }
                rule 60 {
                    action drop
                    description "(IPv4) [DROP] - CAPTIVE to ANY"
                    source {
                        group {
                            network-group PFX-RESEL-USER-CAPTIVE-V4
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                }
                /* User hardening SSH rules */
                rule 100 {
                    action accept
                    description "(IPv4) [ACCEPT] - USER to JUMPS - SSH"
                    destination {
                        group {
                            network-group PFX-RESEL-JUMPS-V4
                        }
                        port ssh
                    }
                    inbound-interface {
                        group VRF-RESEL-USER-1
                    }
                    protocol tcp
                }
                rule 110 {
                    action accept
                    description "(IPv4) [ACCEPT] - USER to DMZ - SSH (for GitLab)"
                    destination {
                        group {
                            network-group PFX-RESEL-DMZ-RP-V4
                        }
                        port ssh
                    }
                    inbound-interface {
                        group VRF-RESEL-USER-1
                    }
                    protocol tcp
                }
                /* DHCP rules (check if they are necessary - Because of helper IP) */
                rule 200 {
                    action accept
                    description "(IPv4) [ACCEPT] - USER to SYSTEM - DHCP"
                    destination {
                        group {
                            network-group PFX-RESEL-DHCP-V4
                        }
                        port 67
                    }
                    inbound-interface {
                        group VRF-RESEL-USER-1
                    }
                    protocol udp
                }
                rule 210 {
                    action accept
                    description "(IPv4) [ACCEPT] - AP to SYSTEM - DHCP"
                    destination {
                        group {
                            network-group PFX-RESEL-DHCP-V4
                        }
                        port 67
                    }
                    inbound-interface {
                        group VRF-RESEL-AP
                    }
                    protocol udp
                }
                /* SIEM rules */
                rule 300 {
                    action accept
                    description "(IPv4) [ACCEPT] - DMZ to SYSTEM - SIEM (1514)"
                    destination {
                        group {
                            network-group PFX-RESEL-SIEM-V4
                        }
                        port 1514
                    }
                    inbound-interface {
                        group VRF-RESEL-DMZ
                    }
                    protocol udp
                    source {
                        group {
                            network-group PFX-RESEL-DMZ-V4
                        }
                    }
                }
                rule 350 {
                    action accept
                    description "(IPv4) [ACCEPT] - DMZ to SYSTEM - SIEM (1515)"
                    destination {
                        group {
                            network-group PFX-RESEL-SIEM-V4
                        }
                        port 1515
                    }
                    inbound-interface {
                        group VRF-RESEL-DMZ
                    }
                    protocol udp
                    source {
                        group {
                            network-group PFX-RESEL-DMZ-V4
                        }
                    }
                }
                rule 900 {
                    action drop
                    description "(IPv4) [DROP] - USER to SYSTEM"
                    destination {
                        group {
                            network-group PFX-RESEL-V4
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-USER-1
                    }
                    protocol tcp
                }
                /* Internal service rules */
                rule 1100 {
                    action accept
                    description "(IPv4) [ACCEPT] - WARZONE to DMZ"
                    destination {
                        group {
                            network-group PFX-RESEL-DMZ-V4
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                    source {
                        group {
                            network-group PFX-RESEL-WARZONE-V4
                        }
                    }
                }
                rule 1200 {
                    action accept
                    description "(IPv4) [ACCEPT] - USER to DMZ"
                    destination {
                        group {
                            network-group PFX-RESEL-DMZ-V4
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-USER-1
                    }
                }
                rule 1310 {
                    action accept
                    description "(IPv4) [ACCEPT] - AP to SYSTEM - RADIUS"
                    destination {
                        group {
                            network-group PFX-RESEL-RADIUS-V4
                        }
                        port 1812,1813
                    }
                    inbound-interface {
                        group VRF-RESEL-AP
                    }
                    protocol udp
                }
                
                /* This rule needs to be hardened to only allow specific services and destination IPs */
                rule 1315 {
                    action accept
                    description "(IPv4) [ACCEPT] - AP to SYSTEM - other"
                    destination {
                        group {
                            network-group PFX-RESEL-SYSTEM-V4
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-AP
                    }
                }
                /* This rule needs to be hardened to only allow specific services and destination IPs */
                rule 1350 {
                    action accept
                    description "(IPv4) [ACCEPT] - AP to DMZ"
                    destination {
                        group {
                            network-group PFX-RESEL-DMZ-V4
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-AP
                    }
                }
                /* Management rules */
                rule 2100 {
                    action accept
                    description "(IPv4) [ACCEPT] - SYSTEM ADMINS to ALL"
                    destination {
                        group {
                            network-group PFX-RESEL-V4
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-SYSTEM
                    }
                    source {
                        group {
                            network-group PFX-RESEL-ADMINS-V4
                        }
                    }
                }
                /* Inter-VRF trafic, drop by default */
                rule 7100 {
                    action drop
                    description "(IPv4) [DROP] - ANY to AP"
                    outbound-interface {
                        group VRF-RESEL-AP
                    }
                }
                rule 7200 {
                    action drop
                    description "(IPv4) [DROP] - ANY to DMZ"
                    outbound-interface {
                        group VRF-RESEL-DMZ
                    }
                }
                rule 7300 {
                    action drop
                    description "(IPv4) [DROP] - ANY to PUBLIC"
                    outbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                }
                rule 7400 {
                    action drop
                    description "(IPv4) [DROP] - ANY to SYSTEM"
                    outbound-interface {
                        group VRF-RESEL-SYSTEM
                    }
                }
                rule 7500 {
                    action drop
                    description "(IPv4) [DROP] - ANY to USER"
                    outbound-interface {
                        group VRF-RESEL-USER-1
                    }
                }
                /* Egress Internet access */
                rule 8100 {
                    action accept
                    description "(IPv4) [ACCEPT] - DMZ to INTERNET"
                    destination {
                        group {
                            network-group "NG-DEFAULT-V4"
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-DMZ
                    }
                }
                rule 8200 {
                    action accept
                    description "(IPv4) [ACCEPT] - AP to INTERNET"
                    destination {
                        group {
                            network-group "NG-DEFAULT-V4"
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-AP
                    }
                }
                rule 8300 {
                    action accept
                    description "(IPv4) [ACCEPT] - SYSTEM to INTERNET"
                    destination {
                        group {
                            network-group "NG-DEFAULT-V4"
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-SYSTEM
                    }
                }
                rule 8400 {
                    action accept
                    description "(IPv4) [ACCEPT] - PUBLIC to INTERNET"
                    destination {
                        group {
                            network-group "NG-DEFAULT-V4"
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-PUBLIC
                    }
                }
                rule 8500 {
                    action accept
                    description "(IPv4) [ACCEPT] - USER to INTERNET"
                    destination {
                        group {
                            network-group "NG-DEFAULT-V4"
                        }
                    }
                    inbound-interface {
                        group VRF-RESEL-USER-1
                    }
                }
                /* Ingress Internet rules */
                rule 9100 {
                    action accept
                    description "(IPv4) [ACCEPT] - INTERNET to DMZ - DNS PAT"
                    destination {
                        group {
                            network-group PFX-RESEL-DNS-V4
                        }
                        port 53
                    }
                    inbound-interface {
                        group VRF-RESEL-MAIN
                    }
                    protocol tcp_udp
                }
                rule 9200 {
                    action accept
                    description "(IPv4) [ACCEPT] - INTERNET to DMZ - MAIL PAT"
                    destination {
                        group {
                            network-group PFX-RESEL-MAIL-V4
                        }
                        port imap,imaps,smtp,smtps,pop3,pop3s,587
                    }
                    inbound-interface {
                        group VRF-RESEL-MAIN
                    }
                    protocol tcp
                }
                /* Explicit default drop */
                rule 10000 {
                    action "drop"
                }
            }
        }
        input {
            filter {
                default-log
            }
        }
        output {
            filter {
                default-log
            }
        }
    }
    ipv6 {
        forward {
            filter {
                default-log
                rule 10 {
                    action "accept"
                    description "(IPv6) [ACCEPT] - ESTABLISHED CONNECTIONS"
                    state "established"
                    state "related"
                }
                /* Egress Internet access */
                rule 8000 {
                    action "accept"
                    description "(IPv6) [ACCEPT] - USER to INTERNET"
                    destination {
                        group {
                            network-group "NG-DEFAULT-V6"
                        }
                    }
                    source {
                        group {
                            network-group "NG-RESEL-SUPERNET-V6"
                        }
                    }
                }
                rule 10000 {
                    action "drop"
                }
            }
        }
        input {
            filter {
                default-log
            }
        }
        output {
            filter {
                default-log
            }
        }
    }
}
interfaces {
    dummy dum0 {
        address "89.234.163.0/32"
        address "89.234.163.1/32"
        address "89.234.163.2/32"
        address "89.234.163.3/32"
        address "89.234.163.4/32"
        address "89.234.163.5/32"
        address "89.234.163.6/32"
        address "89.234.163.7/32"
        address "89.234.163.8/32"
        address "89.234.163.9/32"
        address "89.234.163.10/32"
        address "89.234.163.11/32"
        address "89.234.163.12/32"
        address "89.234.163.13/32"
        address "89.234.163.14/32"
        address "89.234.163.15/32"
        address "89.234.163.16/32"
        address "89.234.163.17/32"
        address "89.234.163.18/32"
        address "89.234.163.19/32"
        address "89.234.163.20/32"
        address "89.234.163.21/32"
        address "89.234.163.22/32"
        address "89.234.163.23/32"
        address "89.234.163.24/32"
        address "89.234.163.25/32"
        address "89.234.163.26/32"
        address "89.234.163.27/32"
        address "89.234.163.28/32"
        address "89.234.163.29/32"
        address "89.234.163.30/32"
        address "89.234.163.31/32"
        address "89.234.163.32/32"
        address "89.234.163.33/32"
        address "89.234.163.34/32"
        address "89.234.163.35/32"
        address "89.234.163.36/32"
        address "89.234.163.37/32"
        address "89.234.163.38/32"
        address "89.234.163.39/32"
        address "89.234.163.40/32"
        address "89.234.163.41/32"
        address "89.234.163.42/32"
        address "89.234.163.43/32"
        address "89.234.163.44/32"
        address "89.234.163.45/32"
        address "89.234.163.46/32"
        address "89.234.163.47/32"
        address "89.234.163.48/32"
        address "89.234.163.49/32"
        address "89.234.163.50/32"
        address "89.234.163.51/32"
        address "89.234.163.52/32"
        address "89.234.163.53/32"
        address "89.234.163.54/32"
        address "89.234.163.55/32"
        address "89.234.163.56/32"
        address "89.234.163.57/32"
        address "89.234.163.58/32"
        address "89.234.163.59/32"
        address "89.234.163.60/32"
        address "89.234.163.61/32"
        address "89.234.163.62/32"
        address "89.234.163.63/32"
        address "89.234.163.64/32"
        address "89.234.163.65/32"
        address "89.234.163.66/32"
        address "89.234.163.67/32"
        address "89.234.163.68/32"
        address "89.234.163.69/32"
        address "89.234.163.70/32"
        address "89.234.163.71/32"
        address "89.234.163.72/32"
        address "89.234.163.73/32"
        address "89.234.163.74/32"
        address "89.234.163.75/32"
        address "89.234.163.76/32"
        address "89.234.163.77/32"
        address "89.234.163.78/32"
        address "89.234.163.79/32"
        address "89.234.163.80/32"
        address "89.234.163.81/32"
        address "89.234.163.82/32"
        address "89.234.163.83/32"
        address "89.234.163.84/32"
        address "89.234.163.85/32"
        address "89.234.163.86/32"
        address "89.234.163.87/32"
        address "89.234.163.88/32"
        address "89.234.163.89/32"
        address "89.234.163.90/32"
        address "89.234.163.91/32"
        address "89.234.163.92/32"
        address "89.234.163.93/32"
        address "89.234.163.94/32"
        address "89.234.163.95/32"
        address "89.234.163.96/32"
        address "89.234.163.97/32"
        address "89.234.163.98/32"
        address "89.234.163.99/32"
        address "89.234.163.100/32"
        address "89.234.163.101/32"
        address "89.234.163.102/32"
        address "89.234.163.103/32"
        address "89.234.163.104/32"
        address "89.234.163.105/32"
        address "89.234.163.106/32"
        address "89.234.163.107/32"
        address "89.234.163.108/32"
        address "89.234.163.109/32"
        address "89.234.163.110/32"
        address "89.234.163.111/32"
        address "89.234.163.112/32"
        address "89.234.163.113/32"
        address "89.234.163.114/32"
        address "89.234.163.115/32"
        address "89.234.163.116/32"
        address "89.234.163.117/32"
        address "89.234.163.118/32"
        address "89.234.163.119/32"
        address "89.234.163.120/32"
        address "89.234.163.121/32"
        address "89.234.163.122/32"
        address "89.234.163.123/32"
        address "89.234.163.124/32"
        address "89.234.163.125/32"
        address "89.234.163.126/32"
        address "89.234.163.127/32"
        address "89.234.163.128/32"
        address "89.234.163.129/32"
        address "89.234.163.130/32"
        address "89.234.163.131/32"
        address "89.234.163.132/32"
        address "89.234.163.133/32"
        address "89.234.163.134/32"
        address "89.234.163.135/32"
        address "89.234.163.136/32"
        address "89.234.163.137/32"
        address "89.234.163.138/32"
        address "89.234.163.139/32"
        address "89.234.163.140/32"
        address "89.234.163.141/32"
        address "89.234.163.142/32"
        address "89.234.163.143/32"
        address "89.234.163.144/32"
        address "89.234.163.145/32"
        address "89.234.163.146/32"
        address "89.234.163.147/32"
        address "89.234.163.148/32"
        address "89.234.163.149/32"
        address "89.234.163.150/32"
        address "89.234.163.151/32"
        address "89.234.163.152/32"
        address "89.234.163.153/32"
        address "89.234.163.154/32"
        address "89.234.163.155/32"
        address "89.234.163.156/32"
        address "89.234.163.157/32"
        address "89.234.163.158/32"
        address "89.234.163.159/32"
        address "89.234.163.160/32"
        address "89.234.163.161/32"
        address "89.234.163.162/32"
        address "89.234.163.163/32"
        address "89.234.163.164/32"
        address "89.234.163.165/32"
        address "89.234.163.166/32"
        address "89.234.163.167/32"
        address "89.234.163.168/32"
        address "89.234.163.169/32"
        address "89.234.163.170/32"
        address "89.234.163.171/32"
        address "89.234.163.172/32"
        address "89.234.163.173/32"
        address "89.234.163.174/32"
        address "89.234.163.175/32"
        address "89.234.163.176/32"
        address "89.234.163.177/32"
        address "89.234.163.178/32"
        address "89.234.163.179/32"
        address "89.234.163.180/32"
        address "89.234.163.181/32"
        address "89.234.163.182/32"
        address "89.234.163.183/32"
        address "89.234.163.184/32"
        address "89.234.163.185/32"
        address "89.234.163.186/32"
        address "89.234.163.187/32"
        address "89.234.163.188/32"
        address "89.234.163.189/32"
        address "89.234.163.190/32"
        address "89.234.163.191/32"
        address "89.234.163.192/32"
        address "89.234.163.193/32"
        address "89.234.163.194/32"
        address "89.234.163.195/32"
        address "89.234.163.196/32"
        address "89.234.163.197/32"
        address "89.234.163.198/32"
        address "89.234.163.199/32"
        address "89.234.163.200/32"
        address "89.234.163.201/32"
        address "89.234.163.202/32"
        address "89.234.163.203/32"
        address "89.234.163.204/32"
        address "89.234.163.205/32"
        address "89.234.163.206/32"
        address "89.234.163.207/32"
        address "89.234.163.208/32"
        address "89.234.163.209/32"
        address "89.234.163.210/32"
        address "89.234.163.211/32"
        address "89.234.163.212/32"
        address "89.234.163.213/32"
        address "89.234.163.214/32"
        address "89.234.163.215/32"
        address "89.234.163.216/32"
        address "89.234.163.217/32"
        address "89.234.163.218/32"
        address "89.234.163.219/32"
        address "89.234.163.220/32"
        address "89.234.163.221/32"
        address "89.234.163.222/32"
        address "89.234.163.223/32"
        address "89.234.163.224/32"
        address "89.234.163.225/32"
        address "89.234.163.226/32"
        address "89.234.163.227/32"
        address "89.234.163.228/32"
        address "89.234.163.229/32"
        address "89.234.163.230/32"
        address "89.234.163.231/32"
        address "89.234.163.232/32"
        address "89.234.163.233/32"
        address "89.234.163.234/32"
        address "89.234.163.235/32"
        address "89.234.163.236/32"
        address "89.234.163.237/32"
        address "89.234.163.238/32"
        address "89.234.163.239/32"
        address "89.234.163.240/32"
        address "89.234.163.241/32"
        address "89.234.163.242/32"
        address "89.234.163.243/32"
        address "89.234.163.244/32"
        address "89.234.163.245/32"
        address "89.234.163.246/32"
        address "89.234.163.247/32"
        address "89.234.163.248/32"
        address "89.234.163.249/32"
        address "89.234.163.250/32"
        address "89.234.163.251/32"
        address "89.234.163.252/32"
        address "89.234.163.253/32"
        address "89.234.163.254/32"
        address "89.234.163.255/32"
        address "2a00:5881:3080::1/44"
    }
    ethernet eth1 {
        address "100.84.132.32/31"
        address "2a00:5881:3080:100::84:132:32/127"
        description "RESEL-MAIN-CORE1-NODAL"
        hw-id "bc:24:11:bc:94:b3"
    }
    ethernet eth2 {
        address "100.84.132.34/31"
        address "2a00:5881:3080:100::84:132:34/127"
        description "RESEL-AP-CORE1-NODAL"
        hw-id "bc:24:11:76:a1:36"
    }
    ethernet eth3 {
        address "100.84.132.36/31"
        address "2a00:5881:3080:100::84:132:36/127"
        description "RESEL-DMZ-CORE1-NODAL"
        hw-id "bc:24:11:fa:ab:25"
    }
    ethernet eth4 {
        address "100.84.132.38/31"
        address "2a00:5881:3080:100::84:132:38/127"
        description "RESEL-PUBLIC-CORE1-NODAL"
        hw-id "bc:24:11:1a:97:4d"
    }
    ethernet eth5 {
        address "100.84.132.40/31"
        address "2a00:5881:3080:100::84:132:40/127"
        description "RESEL-SYSTEM-CORE1-NODAL"
        hw-id "bc:24:11:fe:a2:3a"
    }
    ethernet eth6 {
        address "100.84.132.42/31"
        address "2a00:5881:3080:100::84:132:42/127"
        description "RESEL-USER-1-CORE1-NODAL"
        hw-id "bc:24:11:5f:b9:0a"
    }
    ethernet eth7 {
        address "10.35.9.102/16"
        description "RESEL-MGMT-SYSTEM"
        hw-id "bc:24:11:6c:67:34"
    }
    loopback lo {
    }
}
nat {
    destination {
        rule 20 {
            description "SSH CHEVREUIL"
            destination {
                address "89.234.163.248"
                port "22"
            }
            protocol "tcp"
            translation {
                address "10.34.255.1"
            }
        }
        rule 30 {
            description "DNS RENNES"
            destination {
                address "89.234.163.251"
                port "53"
            }
            protocol "tcp_udp"
            translation {
                address "10.36.13.2"
            }
        }
    }
    source {
        rule 10 {
            description "NAT SORTANT DNS"
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                address "10.36.13.2"
            }
            translation {
                address "89.234.163.251"
            }
        }
        rule 100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                address "100.84.132.32"
            }
            translation {
                address "89.234.163.248"
            }
        }
        rule 110 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                address "100.84.133.33"
            }
            translation {
                address "89.234.163.252"
            }
        }
        rule 200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-V4"
                }
            }
            translation {
                address "89.234.163.252"
            }
        }
        rule 1000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-UNKNOWN-V4"
                }
            }
            translation {
                address "89.234.163.0"
            }
        }
        rule 1100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2751-V4"
                }
            }
            translation {
                address "89.234.163.1"
            }
        }
        rule 1200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2752-V4"
                }
            }
            translation {
                address "89.234.163.2"
            }
        }
        rule 1300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2753-V4"
                }
            }
            translation {
                address "89.234.163.3"
            }
        }
        rule 1400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2754-V4"
                }
            }
            translation {
                address "89.234.163.4"
            }
        }
        rule 1500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2755-V4"
                }
            }
            translation {
                address "89.234.163.5"
            }
        }
        rule 1600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2756-V4"
                }
            }
            translation {
                address "89.234.163.6"
            }
        }
        rule 1700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2757-V4"
                }
            }
            translation {
                address "89.234.163.7"
            }
        }
        rule 1800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2758-V4"
                }
            }
            translation {
                address "89.234.163.8"
            }
        }
        rule 1900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2759-V4"
                }
            }
            translation {
                address "89.234.163.9"
            }
        }
        rule 2000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2760-V4"
                }
            }
            translation {
                address "89.234.163.10"
            }
        }
        rule 2100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2761-V4"
                }
            }
            translation {
                address "89.234.163.11"
            }
        }
        rule 2200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2762-V4"
                }
            }
            translation {
                address "89.234.163.12"
            }
        }
        rule 2300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2763-V4"
                }
            }
            translation {
                address "89.234.163.13"
            }
        }
        rule 2400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2764-V4"
                }
            }
            translation {
                address "89.234.163.14"
            }
        }
        rule 2500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2765-V4"
                }
            }
            translation {
                address "89.234.163.15"
            }
        }
        rule 2600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2766-V4"
                }
            }
            translation {
                address "89.234.163.16"
            }
        }
        rule 2700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2767-V4"
                }
            }
            translation {
                address "89.234.163.17"
            }
        }
        rule 2800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2768-V4"
                }
            }
            translation {
                address "89.234.163.18"
            }
        }
        rule 2900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2769-V4"
                }
            }
            translation {
                address "89.234.163.19"
            }
        }
        rule 3000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2770-V4"
                }
            }
            translation {
                address "89.234.163.20"
            }
        }
        rule 3100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2771-V4"
                }
            }
            translation {
                address "89.234.163.21"
            }
        }
        rule 3200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2772-V4"
                }
            }
            translation {
                address "89.234.163.22"
            }
        }
        rule 3300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2773-V4"
                }
            }
            translation {
                address "89.234.163.23"
            }
        }
        rule 3400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2774-V4"
                }
            }
            translation {
                address "89.234.163.24"
            }
        }
        rule 3500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2775-V4"
                }
            }
            translation {
                address "89.234.163.25"
            }
        }
        rule 3600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2776-V4"
                }
            }
            translation {
                address "89.234.163.26"
            }
        }
        rule 3700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2777-V4"
                }
            }
            translation {
                address "89.234.163.27"
            }
        }
        rule 3800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2778-V4"
                }
            }
            translation {
                address "89.234.163.28"
            }
        }
        rule 3900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2779-V4"
                }
            }
            translation {
                address "89.234.163.29"
            }
        }
        rule 4000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2780-V4"
                }
            }
            translation {
                address "89.234.163.30"
            }
        }
        rule 4100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2781-V4"
                }
            }
            translation {
                address "89.234.163.31"
            }
        }
        rule 4200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2782-V4"
                }
            }
            translation {
                address "89.234.163.32"
            }
        }
        rule 4300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2783-V4"
                }
            }
            translation {
                address "89.234.163.33"
            }
        }
        rule 4400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2784-V4"
                }
            }
            translation {
                address "89.234.163.34"
            }
        }
        rule 4500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2785-V4"
                }
            }
            translation {
                address "89.234.163.35"
            }
        }
        rule 4600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2786-V4"
                }
            }
            translation {
                address "89.234.163.36"
            }
        }
        rule 4700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2787-V4"
                }
            }
            translation {
                address "89.234.163.37"
            }
        }
        rule 4800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2788-V4"
                }
            }
            translation {
                address "89.234.163.38"
            }
        }
        rule 4900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2789-V4"
                }
            }
            translation {
                address "89.234.163.39"
            }
        }
        rule 5000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2790-V4"
                }
            }
            translation {
                address "89.234.163.40"
            }
        }
        rule 5100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2791-V4"
                }
            }
            translation {
                address "89.234.163.41"
            }
        }
        rule 5200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2792-V4"
                }
            }
            translation {
                address "89.234.163.42"
            }
        }
        rule 5300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2793-V4"
                }
            }
            translation {
                address "89.234.163.43"
            }
        }
        rule 5400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2794-V4"
                }
            }
            translation {
                address "89.234.163.44"
            }
        }
        rule 5500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2795-V4"
                }
            }
            translation {
                address "89.234.163.45"
            }
        }
        rule 5600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2796-V4"
                }
            }
            translation {
                address "89.234.163.46"
            }
        }
        rule 5700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2797-V4"
                }
            }
            translation {
                address "89.234.163.47"
            }
        }
        rule 5800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2798-V4"
                }
            }
            translation {
                address "89.234.163.48"
            }
        }
        rule 5900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2799-V4"
                }
            }
            translation {
                address "89.234.163.49"
            }
        }
        rule 6000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2800-V4"
                }
            }
            translation {
                address "89.234.163.50"
            }
        }
        rule 6100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2801-V4"
                }
            }
            translation {
                address "89.234.163.51"
            }
        }
        rule 6200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2802-V4"
                }
            }
            translation {
                address "89.234.163.52"
            }
        }
        rule 6300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2803-V4"
                }
            }
            translation {
                address "89.234.163.53"
            }
        }
        rule 6400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2804-V4"
                }
            }
            translation {
                address "89.234.163.54"
            }
        }
        rule 6500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2805-V4"
                }
            }
            translation {
                address "89.234.163.55"
            }
        }
        rule 6600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2806-V4"
                }
            }
            translation {
                address "89.234.163.56"
            }
        }
        rule 6700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2807-V4"
                }
            }
            translation {
                address "89.234.163.57"
            }
        }
        rule 6800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2808-V4"
                }
            }
            translation {
                address "89.234.163.58"
            }
        }
        rule 6900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2809-V4"
                }
            }
            translation {
                address "89.234.163.59"
            }
        }
        rule 7000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2810-V4"
                }
            }
            translation {
                address "89.234.163.60"
            }
        }
        rule 7100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2811-V4"
                }
            }
            translation {
                address "89.234.163.61"
            }
        }
        rule 7200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2812-V4"
                }
            }
            translation {
                address "89.234.163.62"
            }
        }
        rule 7300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2813-V4"
                }
            }
            translation {
                address "89.234.163.63"
            }
        }
        rule 7400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2814-V4"
                }
            }
            translation {
                address "89.234.163.64"
            }
        }
        rule 7500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2815-V4"
                }
            }
            translation {
                address "89.234.163.65"
            }
        }
        rule 7600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2816-V4"
                }
            }
            translation {
                address "89.234.163.66"
            }
        }
        rule 7700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2817-V4"
                }
            }
            translation {
                address "89.234.163.67"
            }
        }
        rule 7800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2818-V4"
                }
            }
            translation {
                address "89.234.163.68"
            }
        }
        rule 7900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2819-V4"
                }
            }
            translation {
                address "89.234.163.69"
            }
        }
        rule 8000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2820-V4"
                }
            }
            translation {
                address "89.234.163.70"
            }
        }
        rule 8100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2821-V4"
                }
            }
            translation {
                address "89.234.163.71"
            }
        }
        rule 8200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2822-V4"
                }
            }
            translation {
                address "89.234.163.72"
            }
        }
        rule 8300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2823-V4"
                }
            }
            translation {
                address "89.234.163.73"
            }
        }
        rule 8400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2824-V4"
                }
            }
            translation {
                address "89.234.163.74"
            }
        }
        rule 8500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2825-V4"
                }
            }
            translation {
                address "89.234.163.75"
            }
        }
        rule 8600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2826-V4"
                }
            }
            translation {
                address "89.234.163.76"
            }
        }
        rule 8700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2827-V4"
                }
            }
            translation {
                address "89.234.163.77"
            }
        }
        rule 8800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2828-V4"
                }
            }
            translation {
                address "89.234.163.78"
            }
        }
        rule 8900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2829-V4"
                }
            }
            translation {
                address "89.234.163.79"
            }
        }
        rule 9000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2830-V4"
                }
            }
            translation {
                address "89.234.163.80"
            }
        }
        rule 9100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2831-V4"
                }
            }
            translation {
                address "89.234.163.81"
            }
        }
        rule 9200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2832-V4"
                }
            }
            translation {
                address "89.234.163.82"
            }
        }
        rule 9300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2833-V4"
                }
            }
            translation {
                address "89.234.163.83"
            }
        }
        rule 9400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2834-V4"
                }
            }
            translation {
                address "89.234.163.84"
            }
        }
        rule 9500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2835-V4"
                }
            }
            translation {
                address "89.234.163.85"
            }
        }
        rule 9600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2836-V4"
                }
            }
            translation {
                address "89.234.163.86"
            }
        }
        rule 9700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2837-V4"
                }
            }
            translation {
                address "89.234.163.87"
            }
        }
        rule 9800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2838-V4"
                }
            }
            translation {
                address "89.234.163.88"
            }
        }
        rule 9900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2839-V4"
                }
            }
            translation {
                address "89.234.163.89"
            }
        }
        rule 10000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2840-V4"
                }
            }
            translation {
                address "89.234.163.90"
            }
        }
        rule 10100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2841-V4"
                }
            }
            translation {
                address "89.234.163.91"
            }
        }
        rule 10200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2842-V4"
                }
            }
            translation {
                address "89.234.163.92"
            }
        }
        rule 10300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2843-V4"
                }
            }
            translation {
                address "89.234.163.93"
            }
        }
        rule 10400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2844-V4"
                }
            }
            translation {
                address "89.234.163.94"
            }
        }
        rule 10500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2845-V4"
                }
            }
            translation {
                address "89.234.163.95"
            }
        }
        rule 10600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2846-V4"
                }
            }
            translation {
                address "89.234.163.96"
            }
        }
        rule 10700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2847-V4"
                }
            }
            translation {
                address "89.234.163.97"
            }
        }
        rule 10800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2848-V4"
                }
            }
            translation {
                address "89.234.163.98"
            }
        }
        rule 10900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2849-V4"
                }
            }
            translation {
                address "89.234.163.99"
            }
        }
        rule 11000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2850-V4"
                }
            }
            translation {
                address "89.234.163.100"
            }
        }
        rule 11100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2851-V4"
                }
            }
            translation {
                address "89.234.163.101"
            }
        }
        rule 11200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2852-V4"
                }
            }
            translation {
                address "89.234.163.102"
            }
        }
        rule 11300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2853-V4"
                }
            }
            translation {
                address "89.234.163.103"
            }
        }
        rule 11400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2854-V4"
                }
            }
            translation {
                address "89.234.163.104"
            }
        }
        rule 11500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2855-V4"
                }
            }
            translation {
                address "89.234.163.105"
            }
        }
        rule 11600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2856-V4"
                }
            }
            translation {
                address "89.234.163.106"
            }
        }
        rule 11700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2857-V4"
                }
            }
            translation {
                address "89.234.163.107"
            }
        }
        rule 11800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2858-V4"
                }
            }
            translation {
                address "89.234.163.108"
            }
        }
        rule 11900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2859-V4"
                }
            }
            translation {
                address "89.234.163.109"
            }
        }
        rule 12000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2860-V4"
                }
            }
            translation {
                address "89.234.163.110"
            }
        }
        rule 12100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2861-V4"
                }
            }
            translation {
                address "89.234.163.111"
            }
        }
        rule 12200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2862-V4"
                }
            }
            translation {
                address "89.234.163.112"
            }
        }
        rule 12300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2863-V4"
                }
            }
            translation {
                address "89.234.163.113"
            }
        }
        rule 12400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2864-V4"
                }
            }
            translation {
                address "89.234.163.114"
            }
        }
        rule 12500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2865-V4"
                }
            }
            translation {
                address "89.234.163.115"
            }
        }
        rule 12600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2866-V4"
                }
            }
            translation {
                address "89.234.163.116"
            }
        }
        rule 12700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2867-V4"
                }
            }
            translation {
                address "89.234.163.117"
            }
        }
        rule 12800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2868-V4"
                }
            }
            translation {
                address "89.234.163.118"
            }
        }
        rule 12900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2869-V4"
                }
            }
            translation {
                address "89.234.163.119"
            }
        }
        rule 13000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2870-V4"
                }
            }
            translation {
                address "89.234.163.120"
            }
        }
        rule 13100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2871-V4"
                }
            }
            translation {
                address "89.234.163.121"
            }
        }
        rule 13200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2872-V4"
                }
            }
            translation {
                address "89.234.163.122"
            }
        }
        rule 13300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2873-V4"
                }
            }
            translation {
                address "89.234.163.123"
            }
        }
        rule 13400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2874-V4"
                }
            }
            translation {
                address "89.234.163.124"
            }
        }
        rule 13500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2875-V4"
                }
            }
            translation {
                address "89.234.163.125"
            }
        }
        rule 13600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2876-V4"
                }
            }
            translation {
                address "89.234.163.126"
            }
        }
        rule 13700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2877-V4"
                }
            }
            translation {
                address "89.234.163.127"
            }
        }
        rule 13800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2878-V4"
                }
            }
            translation {
                address "89.234.163.128"
            }
        }
        rule 13900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2879-V4"
                }
            }
            translation {
                address "89.234.163.129"
            }
        }
        rule 14000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2880-V4"
                }
            }
            translation {
                address "89.234.163.130"
            }
        }
        rule 14100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2881-V4"
                }
            }
            translation {
                address "89.234.163.131"
            }
        }
        rule 14200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2882-V4"
                }
            }
            translation {
                address "89.234.163.132"
            }
        }
        rule 14300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2883-V4"
                }
            }
            translation {
                address "89.234.163.133"
            }
        }
        rule 14400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2884-V4"
                }
            }
            translation {
                address "89.234.163.134"
            }
        }
        rule 14500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2885-V4"
                }
            }
            translation {
                address "89.234.163.135"
            }
        }
        rule 14600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2886-V4"
                }
            }
            translation {
                address "89.234.163.136"
            }
        }
        rule 14700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2887-V4"
                }
            }
            translation {
                address "89.234.163.137"
            }
        }
        rule 14800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2888-V4"
                }
            }
            translation {
                address "89.234.163.138"
            }
        }
        rule 14900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2889-V4"
                }
            }
            translation {
                address "89.234.163.139"
            }
        }
        rule 15000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2890-V4"
                }
            }
            translation {
                address "89.234.163.140"
            }
        }
        rule 15100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2891-V4"
                }
            }
            translation {
                address "89.234.163.141"
            }
        }
        rule 15200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2892-V4"
                }
            }
            translation {
                address "89.234.163.142"
            }
        }
        rule 15300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2893-V4"
                }
            }
            translation {
                address "89.234.163.143"
            }
        }
        rule 15400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2894-V4"
                }
            }
            translation {
                address "89.234.163.144"
            }
        }
        rule 15500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2895-V4"
                }
            }
            translation {
                address "89.234.163.145"
            }
        }
        rule 15600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2896-V4"
                }
            }
            translation {
                address "89.234.163.146"
            }
        }
        rule 15700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2897-V4"
                }
            }
            translation {
                address "89.234.163.147"
            }
        }
        rule 15800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2898-V4"
                }
            }
            translation {
                address "89.234.163.148"
            }
        }
        rule 15900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2899-V4"
                }
            }
            translation {
                address "89.234.163.149"
            }
        }
        rule 16000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2900-V4"
                }
            }
            translation {
                address "89.234.163.150"
            }
        }
        rule 16100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2901-V4"
                }
            }
            translation {
                address "89.234.163.151"
            }
        }
        rule 16200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2902-V4"
                }
            }
            translation {
                address "89.234.163.152"
            }
        }
        rule 16300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2903-V4"
                }
            }
            translation {
                address "89.234.163.153"
            }
        }
        rule 16400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2904-V4"
                }
            }
            translation {
                address "89.234.163.154"
            }
        }
        rule 16500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2905-V4"
                }
            }
            translation {
                address "89.234.163.155"
            }
        }
        rule 16600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2906-V4"
                }
            }
            translation {
                address "89.234.163.156"
            }
        }
        rule 16700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2907-V4"
                }
            }
            translation {
                address "89.234.163.157"
            }
        }
        rule 16800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2908-V4"
                }
            }
            translation {
                address "89.234.163.158"
            }
        }
        rule 16900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2909-V4"
                }
            }
            translation {
                address "89.234.163.159"
            }
        }
        rule 17000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2910-V4"
                }
            }
            translation {
                address "89.234.163.160"
            }
        }
        rule 17100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2911-V4"
                }
            }
            translation {
                address "89.234.163.161"
            }
        }
        rule 17200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2912-V4"
                }
            }
            translation {
                address "89.234.163.162"
            }
        }
        rule 17300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2913-V4"
                }
            }
            translation {
                address "89.234.163.163"
            }
        }
        rule 17400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2914-V4"
                }
            }
            translation {
                address "89.234.163.164"
            }
        }
        rule 17500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2915-V4"
                }
            }
            translation {
                address "89.234.163.165"
            }
        }
        rule 17600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2916-V4"
                }
            }
            translation {
                address "89.234.163.166"
            }
        }
        rule 17700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2917-V4"
                }
            }
            translation {
                address "89.234.163.167"
            }
        }
        rule 17800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2918-V4"
                }
            }
            translation {
                address "89.234.163.168"
            }
        }
        rule 17900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2919-V4"
                }
            }
            translation {
                address "89.234.163.169"
            }
        }
        rule 18000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2920-V4"
                }
            }
            translation {
                address "89.234.163.170"
            }
        }
        rule 18100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2921-V4"
                }
            }
            translation {
                address "89.234.163.171"
            }
        }
        rule 18200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2922-V4"
                }
            }
            translation {
                address "89.234.163.172"
            }
        }
        rule 18300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2923-V4"
                }
            }
            translation {
                address "89.234.163.173"
            }
        }
        rule 18400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2924-V4"
                }
            }
            translation {
                address "89.234.163.174"
            }
        }
        rule 18500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2925-V4"
                }
            }
            translation {
                address "89.234.163.175"
            }
        }
        rule 18600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2926-V4"
                }
            }
            translation {
                address "89.234.163.176"
            }
        }
        rule 18700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2927-V4"
                }
            }
            translation {
                address "89.234.163.177"
            }
        }
        rule 18800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2928-V4"
                }
            }
            translation {
                address "89.234.163.178"
            }
        }
        rule 18900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2929-V4"
                }
            }
            translation {
                address "89.234.163.179"
            }
        }
        rule 19000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2930-V4"
                }
            }
            translation {
                address "89.234.163.180"
            }
        }
        rule 19100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2931-V4"
                }
            }
            translation {
                address "89.234.163.181"
            }
        }
        rule 19200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2932-V4"
                }
            }
            translation {
                address "89.234.163.182"
            }
        }
        rule 19300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2933-V4"
                }
            }
            translation {
                address "89.234.163.183"
            }
        }
        rule 19400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2934-V4"
                }
            }
            translation {
                address "89.234.163.184"
            }
        }
        rule 19500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2935-V4"
                }
            }
            translation {
                address "89.234.163.185"
            }
        }
        rule 19600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2936-V4"
                }
            }
            translation {
                address "89.234.163.186"
            }
        }
        rule 19700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2937-V4"
                }
            }
            translation {
                address "89.234.163.187"
            }
        }
        rule 19800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2938-V4"
                }
            }
            translation {
                address "89.234.163.188"
            }
        }
        rule 19900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2939-V4"
                }
            }
            translation {
                address "89.234.163.189"
            }
        }
        rule 20000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2940-V4"
                }
            }
            translation {
                address "89.234.163.190"
            }
        }
        rule 20100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2941-V4"
                }
            }
            translation {
                address "89.234.163.191"
            }
        }
        rule 20200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2942-V4"
                }
            }
            translation {
                address "89.234.163.192"
            }
        }
        rule 20300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2943-V4"
                }
            }
            translation {
                address "89.234.163.193"
            }
        }
        rule 20400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2944-V4"
                }
            }
            translation {
                address "89.234.163.194"
            }
        }
        rule 20500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2945-V4"
                }
            }
            translation {
                address "89.234.163.195"
            }
        }
        rule 20600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2946-V4"
                }
            }
            translation {
                address "89.234.163.196"
            }
        }
        rule 20700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2947-V4"
                }
            }
            translation {
                address "89.234.163.197"
            }
        }
        rule 20800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2948-V4"
                }
            }
            translation {
                address "89.234.163.198"
            }
        }
        rule 20900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2949-V4"
                }
            }
            translation {
                address "89.234.163.199"
            }
        }
        rule 21000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2950-V4"
                }
            }
            translation {
                address "89.234.163.200"
            }
        }
        rule 21100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2951-V4"
                }
            }
            translation {
                address "89.234.163.201"
            }
        }
        rule 21200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2952-V4"
                }
            }
            translation {
                address "89.234.163.202"
            }
        }
        rule 21300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2953-V4"
                }
            }
            translation {
                address "89.234.163.203"
            }
        }
        rule 21400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2954-V4"
                }
            }
            translation {
                address "89.234.163.204"
            }
        }
        rule 21500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2955-V4"
                }
            }
            translation {
                address "89.234.163.205"
            }
        }
        rule 21600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2956-V4"
                }
            }
            translation {
                address "89.234.163.206"
            }
        }
        rule 21700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2957-V4"
                }
            }
            translation {
                address "89.234.163.207"
            }
        }
        rule 21800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2958-V4"
                }
            }
            translation {
                address "89.234.163.208"
            }
        }
        rule 21900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2959-V4"
                }
            }
            translation {
                address "89.234.163.209"
            }
        }
        rule 22000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2960-V4"
                }
            }
            translation {
                address "89.234.163.210"
            }
        }
        rule 22100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2961-V4"
                }
            }
            translation {
                address "89.234.163.211"
            }
        }
        rule 22200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2962-V4"
                }
            }
            translation {
                address "89.234.163.212"
            }
        }
        rule 22300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2963-V4"
                }
            }
            translation {
                address "89.234.163.213"
            }
        }
        rule 22400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2964-V4"
                }
            }
            translation {
                address "89.234.163.214"
            }
        }
        rule 22500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2965-V4"
                }
            }
            translation {
                address "89.234.163.215"
            }
        }
        rule 22600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2966-V4"
                }
            }
            translation {
                address "89.234.163.216"
            }
        }
        rule 22700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2967-V4"
                }
            }
            translation {
                address "89.234.163.217"
            }
        }
        rule 22800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2968-V4"
                }
            }
            translation {
                address "89.234.163.218"
            }
        }
        rule 22900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2969-V4"
                }
            }
            translation {
                address "89.234.163.219"
            }
        }
        rule 23000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2970-V4"
                }
            }
            translation {
                address "89.234.163.220"
            }
        }
        rule 23100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2971-V4"
                }
            }
            translation {
                address "89.234.163.221"
            }
        }
        rule 23200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2972-V4"
                }
            }
            translation {
                address "89.234.163.222"
            }
        }
        rule 23300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2973-V4"
                }
            }
            translation {
                address "89.234.163.223"
            }
        }
        rule 23400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2974-V4"
                }
            }
            translation {
                address "89.234.163.224"
            }
        }
        rule 23500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2975-V4"
                }
            }
            translation {
                address "89.234.163.225"
            }
        }
        rule 23600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2976-V4"
                }
            }
            translation {
                address "89.234.163.226"
            }
        }
        rule 23700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2977-V4"
                }
            }
            translation {
                address "89.234.163.227"
            }
        }
        rule 23800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2978-V4"
                }
            }
            translation {
                address "89.234.163.228"
            }
        }
        rule 23900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2979-V4"
                }
            }
            translation {
                address "89.234.163.229"
            }
        }
        rule 24000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2980-V4"
                }
            }
            translation {
                address "89.234.163.230"
            }
        }
        rule 24100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2981-V4"
                }
            }
            translation {
                address "89.234.163.231"
            }
        }
        rule 24200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2982-V4"
                }
            }
            translation {
                address "89.234.163.232"
            }
        }
        rule 24300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2983-V4"
                }
            }
            translation {
                address "89.234.163.233"
            }
        }
        rule 24400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2984-V4"
                }
            }
            translation {
                address "89.234.163.234"
            }
        }
        rule 24500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2985-V4"
                }
            }
            translation {
                address "89.234.163.235"
            }
        }
        rule 24600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2986-V4"
                }
            }
            translation {
                address "89.234.163.236"
            }
        }
        rule 24700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2987-V4"
                }
            }
            translation {
                address "89.234.163.237"
            }
        }
        rule 24800 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2988-V4"
                }
            }
            translation {
                address "89.234.163.238"
            }
        }
        rule 24900 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2989-V4"
                }
            }
            translation {
                address "89.234.163.239"
            }
        }
        rule 25000 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2990-V4"
                }
            }
            translation {
                address "89.234.163.240"
            }
        }
        rule 25100 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2991-V4"
                }
            }
            translation {
                address "89.234.163.241"
            }
        }
        rule 25200 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2992-V4"
                }
            }
            translation {
                address "89.234.163.242"
            }
        }
        rule 25300 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2993-V4"
                }
            }
            translation {
                address "89.234.163.243"
            }
        }
        rule 25400 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2994-V4"
                }
            }
            translation {
                address "89.234.163.244"
            }
        }
        rule 25500 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-2995-V4"
                }
            }
            translation {
                address "89.234.163.245"
            }
        }
        rule 25600 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-WARZONE-V4"
                }
            }
            translation {
                address "89.234.163.246"
            }
        }
        rule 25700 {
            outbound-interface {
                group "VRF-RESEL-MAIN"
            }
            source {
                group {
                    network-group "PFX-RESEL-USER-BDE-V4"
                }
            }
            translation {
                address "89.234.163.247"
            }
        }
    }
}
policy {
    prefix-list PFX-BOGON-V4 {
        rule 10 {
            action "permit"
            le "32"
            prefix "0.0.0.0/8"
        }
        rule 20 {
            action "permit"
            le "32"
            prefix "10.0.0.0/8"
        }
        rule 30 {
            action "permit"
            le "32"
            prefix "100.64.0.0/10"
        }
        rule 40 {
            action "permit"
            le "32"
            prefix "127.0.0.0/8"
        }
        rule 50 {
            action "permit"
            le "32"
            prefix "169.254.0.0/16"
        }
        rule 60 {
            action "permit"
            le "32"
            prefix "172.16.0.0/12"
        }
        rule 70 {
            action "permit"
            le "32"
            prefix "192.0.2.0/24"
        }
        rule 80 {
            action "permit"
            le "32"
            prefix "192.88.99.0/24"
        }
        rule 90 {
            action "permit"
            le "32"
            prefix "192.168.0.0/16"
        }
        rule 100 {
            action "permit"
            le "32"
            prefix "198.18.0.0/15"
        }
        rule 110 {
            action "permit"
            le "32"
            prefix "198.51.100.0/24"
        }
        rule 120 {
            action "permit"
            le "32"
            prefix "203.0.113.0/24"
        }
        rule 130 {
            action "permit"
            le "32"
            prefix "224.0.0.0/4"
        }
        rule 140 {
            action "permit"
            le "32"
            prefix "240.0.0.0/4"
        }
    }
    prefix-list PFX-DEFAULT-V4 {
        rule 10 {
            action "permit"
            prefix "0.0.0.0/0"
        }
    }
    prefix-list PFX-RESEL-BREST-V4 {
        rule 10 {
            action "permit"
            ge "11"
            prefix "10.0.0.0/11"
        }
    }
    prefix-list PFX-RESEL-RENNES-V4 {
        rule 10 {
            action "permit"
            ge "11"
            le "31"
            prefix "10.32.0.0/11"
        }
    }
    prefix-list PFX-RESEL-SUPERNET-ORLONGER-V4 {
        rule 10 {
            action "permit"
            ge "21"
            prefix "89.234.160.0/21"
        }
    }
    prefix-list PFX-RESEL-SUPERNET-V4 {
        rule 10 {
            action "permit"
            prefix "89.234.160.0/21"
        }
    }
    prefix-list6 PFX-BOGON-V6 {
        rule 10 {
            action "permit"
            le "128"
            prefix "::/8"
        }
        rule 20 {
            action "permit"
            le "128"
            prefix "100::/64"
        }
        rule 30 {
            action "permit"
            le "128"
            prefix "2001:2::/48"
        }
        rule 40 {
            action "permit"
            le "128"
            prefix "2001:10::/28"
        }
        rule 50 {
            action "permit"
            le "128"
            prefix "2001:db8::/32"
        }
        rule 60 {
            action "permit"
            le "128"
            prefix "2002::/16"
        }
        rule 70 {
            action "permit"
            le "128"
            prefix "3ffe::/16"
        }
        rule 80 {
            action "permit"
            le "128"
            prefix "fc00::/7"
        }
        rule 90 {
            action "permit"
            le "128"
            prefix "fe80::/10"
        }
        rule 100 {
            action "permit"
            le "128"
            prefix "fec0::/10"
        }
        rule 110 {
            action "permit"
            le "128"
            prefix "ff00::/8"
        }
        rule 120 {
            action "permit"
            le "64"
            prefix "2a00:5881:3081::/48"
        }
    }
    prefix-list6 PFX-DEFAULT-V6 {
        rule 10 {
            action "permit"
            prefix "::/0"
        }
    }
    prefix-list6 PFX-RESEL-SUPERNET-ORLONGER-V6 {
        rule 10 {
            action "permit"
            ge "40"
            prefix "2a00:5881:3000::/40"
        }
        rule 20 {
            action "permit"
            ge "48"
            prefix "2a06:e044:12::/48"
        }
    }
    prefix-list6 PFX-RESEL-SUPERNET-V6 {
        rule 10 {
            action "permit"
            le "48"
            prefix "2a00:5881:3000::/40"
        }
        rule 20 {
            action "permit"
            prefix "2a06:e044:12::/48"
        }
    }
    route-map RM-ACCEPT-BOGON-V4 {
        rule 10 {
            action "permit"
            match {
                ip {
                    address {
                        prefix-list "PFX-BOGON-V4"
                    }
                }
            }
        }
    }
    route-map RM-ACCEPT-BOGON-V6 {
        rule 10 {
            action "permit"
            match {
                ipv6 {
                    address {
                        prefix-list "PFX-BOGON-V6"
                    }
                }
            }
        }
    }
    route-map RM-ACCEPT-DEFAULT-V4 {
        rule 10 {
            action "permit"
            match {
                ip {
                    address {
                        prefix-list "PFX-DEFAULT-V4"
                    }
                }
            }
            set {
                as-path {
                    exclude "all"
                }
            }
        }
    }
    route-map RM-ACCEPT-DEFAULT-V6 {
        rule 10 {
            action "permit"
            match {
                ipv6 {
                    address {
                        prefix-list "PFX-DEFAULT-V6"
                    }
                }
            }
            set {
                as-path {
                    exclude "all"
                }
            }
        }
    }
    route-map RM-ACCEPT-RESEL-BREST-V4 {
        rule 10 {
            action "permit"
            match {
                ip {
                    address {
                        prefix-list "PFX-RESEL-BREST-V4"
                    }
                }
            }
        }
    }
    route-map RM-ACCEPT-RESEL-RENNES-V4 {
        rule 10 {
            action "permit"
            match {
                ip {
                    address {
                        prefix-list "PFX-RESEL-RENNES-V4"
                    }
                }
            }
        }
    }
    route-map RM-ACCEPT-RESEL-SUPERNET-ORLONGER-V4 {
        rule 10 {
            action "permit"
            match {
                ip {
                    address {
                        prefix-list "PFX-RESEL-SUPERNET-ORLONGER-V4"
                    }
                }
            }
        }
    }
    route-map RM-ACCEPT-RESEL-SUPERNET-ORLONGER-V6 {
        rule 10 {
            action "permit"
            match {
                ipv6 {
                    address {
                        prefix-list "PFX-RESEL-SUPERNET-ORLONGER-V6"
                    }
                }
            }
        }
    }
    route-map RM-ACCEPT-RESEL-SUPERNET-V4 {
        rule 10 {
            action "permit"
            match {
                ip {
                    address {
                        prefix-list "PFX-RESEL-SUPERNET-V4"
                    }
                }
            }
        }
    }
    route-map RM-ACCEPT-RESEL-SUPERNET-V6 {
        rule 10 {
            action "permit"
            match {
                ipv6 {
                    address {
                        prefix-list "PFX-RESEL-SUPERNET-V6"
                    }
                }
            }
        }
    }
}
protocols {
    bgp {
        address-family {
            ipv4-unicast {
                redistribute {
                    connected
                }
            }
            ipv6-unicast {
                redistribute {
                    connected
                }
            }
        }
        neighbor 2a00:5881:3080:100::84:132:33 {
            peer-group "PG-CORE-V6"
        }
        neighbor 2a00:5881:3080:100::84:132:35 {
            peer-group "PG-RESEL-AP-V6"
        }
        neighbor 2a00:5881:3080:100::84:132:37 {
            peer-group "PG-RESEL-DMZ-V6"
        }
        neighbor 2a00:5881:3080:100::84:132:39 {
            peer-group "PG-RESEL-PUBLIC-V6"
        }
        neighbor 2a00:5881:3080:100::84:132:41 {
            peer-group "PG-RESEL-SYSTEM-V6"
        }
        neighbor 2a00:5881:3080:100::84:132:43 {
            peer-group "PG-RESEL-USER-1-V6"
        }
        neighbor 100.84.132.33 {
            peer-group "PG-CORE-V4"
        }
        neighbor 100.84.132.35 {
            peer-group "PG-RESEL-AP-V4"
        }
        neighbor 100.84.132.37 {
            peer-group "PG-RESEL-DMZ-V4"
        }
        neighbor 100.84.132.39 {
            peer-group "PG-RESEL-PUBLIC-V4"
        }
        neighbor 100.84.132.41 {
            peer-group "PG-RESEL-SYSTEM-V4"
        }
        neighbor 100.84.132.43 {
            peer-group "PG-RESEL-USER-1-V4"
        }
        parameters {
            always-compare-med
            ebgp-requires-policy
            log-neighbor-changes
        }
        peer-group PG-CORE-V4 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export "RM-ACCEPT-RESEL-SUPERNET-ORLONGER-V4"
                        import "RM-ACCEPT-DEFAULT-V4"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "205669"
        }
        peer-group PG-CORE-V6 {
            address-family {
                ipv6-unicast {
                    route-map {
                        export "RM-ACCEPT-RESEL-SUPERNET-ORLONGER-V6"
                        import "RM-ACCEPT-DEFAULT-V6"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "205669"
        }
        peer-group PG-GWREMOTE1-V4 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export "RM-ACCEPT-RESEL-RENNES-V4"
                        import "RM-ACCEPT-RESEL-BREST-V4"
                    }
                }
            }
            remote-as "4200000001"
        }
        peer-group PG-RESEL-AP-V4 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V4"
                        import "RM-ACCEPT-BOGON-V4"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210000000"
        }
        peer-group PG-RESEL-AP-V6 {
            address-family {
                ipv6-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V6"
                        import "RM-ACCEPT-BOGON-V6"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210000000"
        }
        peer-group PG-RESEL-DMZ-V4 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V4"
                        import "RM-ACCEPT-BOGON-V4"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210001000"
        }
        peer-group PG-RESEL-DMZ-V6 {
            address-family {
                ipv6-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V6"
                        import "RM-ACCEPT-BOGON-V6"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210001000"
        }
        peer-group PG-RESEL-PUBLIC-V4 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V4"
                        import "RM-ACCEPT-BOGON-V4"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210002000"
        }
        peer-group PG-RESEL-PUBLIC-V6 {
            address-family {
                ipv6-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V6"
                        import "RM-ACCEPT-BOGON-V6"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210002000"
        }
        peer-group PG-RESEL-SYSTEM-V4 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V4"
                        import "RM-ACCEPT-BOGON-V4"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210003000"
        }
        peer-group PG-RESEL-SYSTEM-V6 {
            address-family {
                ipv6-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V6"
                        import "RM-ACCEPT-BOGON-V6"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210003000"
        }
        peer-group PG-RESEL-USER-1-V4 {
            address-family {
                ipv4-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V4"
                        import "RM-ACCEPT-BOGON-V4"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210004000"
        }
        peer-group PG-RESEL-USER-1-V6 {
            address-family {
                ipv6-unicast {
                    route-map {
                        export "RM-ACCEPT-DEFAULT-V6"
                        import "RM-ACCEPT-BOGON-V6"
                    }
                    soft-reconfiguration {
                        inbound
                    }
                }
            }
            remote-as "4210004000"
        }
        system-as "4200000000"
    }
}
service {
    ntp {
        allow-client {
            address "0.0.0.0/0"
            address "::/0"
        }
        server time1.vyos.net {
        }
        server time2.vyos.net {
        }
        server time3.vyos.net {
        }
    }
    snmp {
        location "RE-DCIMTA [48.12023, -1.62904]"
        v3 {
            engineid "000000000000000000000002"
            group default {
                mode "ro"
                view "default"
            }
            user librenms {
                auth {
                    encrypted-password "a385be6e7a151238c0f3c25d4a56ce600e91cdaf"
                    type "sha"
                }
                group "default"
                privacy {
                    encrypted-password "f3bba1fe36a0f885c3df5529461eed38f129deaa"
                    type "aes"
                }
            }
            view default {
                oid 1 {
                }
            }
        }
    }
    ssh {
        disable-password-authentication
        port "22"
    }
}
system {
    config-management {
        commit-revisions "100"
    }
    conntrack {
        modules {
            ftp
            h323
            nfs
            pptp
            sip
            sqlnet
            tftp
        }
    }
    console {
        device ttyS0 {
            speed "115200"
        }
    }
    domain-name "intra.resel.fr"
    host-name "gwnat1-re"
    login {
        user admin {
            authentication {
                encrypted-password "$6$rounds=656000$07sVgpNmjIQxMMH4$5aAj0g7quKM3M95MRBa9H1DDx3pfgUun4njV430NSBaqUf5cX.t6vOGsycH5z0f/KwqGQ5UQmqQUQlh5yEPDM."
                public-keys rbelkhir-brest {
                    key "AAAAC3NzaC1lZDI1NTE5AAAAIEOn6zZSwraj8LfXRNMW2cdccewGOZYT9zRBb9EWCP6s"
                    type "ssh-ed25519"
                }
                public-keys rbelkhir-rennes {
                    key "AAAAC3NzaC1lZDI1NTE5AAAAILfqXheCUHNHM7HGkW5Q61ZTa0ahQZNE+8KjVcul6A+7"
                    type "ssh-ed25519"
                }
            }
        }
    }
    name-server "1.1.1.1"
    name-server "8.8.8.8"
    syslog {
        global {
            facility all {
                level "info"
            }
            facility local7 {
                level "debug"
            }
        }
    }
    time-zone "Europe/Paris"
}


// Warning: Do not remove the following line.
// vyos-config-version: "bgp@5:broadcast-relay@1:cluster@2:config-management@1:conntrack@5:conntrack-sync@2:container@2:dhcp-relay@2:dhcp-server@11:dhcpv6-server@5:dns-dynamic@4:dns-forwarding@4:firewall@14:flow-accounting@1:https@6:ids@1:interfaces@32:ipoe-server@3:ipsec@13:isis@3:l2tp@9:lldp@2:mdns@1:monitoring@1:nat@7:nat66@3:ntp@3:openconnect@2:openvpn@1:ospf@2:pim@1:policy@8:pppoe-server@9:pptp@5:qos@2:quagga@11:rip@1:rpki@2:salt@1:snmp@3:ssh@2:sstp@6:system@27:vrf@3:vrrp@4:vyos-accel-ppp@2:wanloadbalance@3:webproxy@2"
// Release version: 1.5-rolling-202404090019

