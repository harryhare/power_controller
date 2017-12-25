clear all,close all,clc

P=8;M=2;%P: prediction length. M: control length.
K=6;L=2;N=K+L; % K: # of servers; L: # of fans
Ps=1400;
Ts=55;
freq_min=4.5;freq_max=36;%max and min dvfs level
fan_min=0.8;fan_max=1; %[Zhirong's fan_min=0.6]
period = 7; % seconds

ip=[];
for i=1:K
    ip=[ip;['192.168.70.', num2str(200+i)]]; % IP addresses of servers 
end

s_port=serial('/dev/ttyUSB1', 'BaudRate', 2400); %[USB] for fan control
fopen(s_port); %[USB]

%--------------- preparing data begin ---------------
slope_s=8;%slope in the linear server power model
slope_f=1; %slope in the linear fan power model %[USB]
slope=[repmat(slope_s,1,K),repmat(slope_f,1,L)];
A=diag(slope); %diagonal matrix form of slope
Gamma=[];Sigma=[]; % Gamma and Sigmma
for i=1:P
    Gamma=[Gamma;A];
    Sigma=blkdiag(Sigma,ones(1,N));
end
SG=Sigma*Gamma;
Psi=zeros(P*N,M*N); %compute Psi
for i=0:M-1 %top part of Psi, which is a diagonal matrix
    Psi(i*N+1:i*N+N,i*N+1:i*N+N)=A;
end
for i=0:P-M-1 %bottom part of Psi
    Psi(M*N+i*N+1:M*N+i*N+N,M*N-N+1:M*N)=(i+2)*A;
    Psi(M*N+i*N+1:M*N+i*N+N,M*N-2*N+1:M*N-N)=-(i+1)*A;
end
Theta=Sigma*Psi; %Theta
ub=repmat( [zeros(K,1);fan_max*(ones(L,1))],M,1 );%upper bound
lb=repmat( [(freq_min-freq_max)*ones(K,1);0.8;fan_min],M,1 );%lower bound
Initial=[(freq_min-freq_max)*ones(M*K,1);0.8*ones(M*L,1)];%start from lower bound
%--------------- preparing data ended ---------------

fwrite(s_port,200);%fwrite(s_port,130); %[USB]
fwrite(s_port,200);%fwrite(s_port,70); %[USB]
fp1=fopen('lev_out.txt','w'); %open a file to write dvfs results to
fp2=fopen('tpower.txt','w'); %open a file to write total power to
tp_out=[];T_out=[];fan_out=[];sum_freq=[];Ps_out=[];
opt=optimset('Algorithm','sqp','Display','off');

fan_power_fit=[132.38,-14.39,15.42,0];
fan_voltage_fit=[1.5158 0.3417,-8.7888,0.7802,47.2451,129.2345];
mu=[0.813571;0.112974];

j=0;
n=60;
cpu_freq = zeros(K,1);
for i=1:K
	% fwrite(t(i),num2str(cpu_freq(i)/4.5,'%.4f\n')); %[tcpip]
	% DVFS_LEVEL = "100";
	% DVFS_LEVEL(2) = num2str(period);
	DVFS_LEVEL = '1';
	if K==1, [a1,a2]=system(['./blade ', ip, ' ', DVFS_LEVEL]);
	else [a1,a2]=system(['./blade ', ip(i,:), ' ', DVFS_LEVEL]); end
	if(a1 ~= 0) fprintf('[DEBUG] Blade-SetFrequency fails.\n'); end
end
pre_level = ones(K,1);

C0 = clock;
D = Initial;
while 1,
    j=j+1

    for i=1:K,
		if K==1, [a1,a2]=system(['./blade ', ip, ' 9']); % get cpu utilization of a blade
		else [a1,a2]=system(['./blade ', ip(i,:), ' 9']); end
		if(a1 == 0)
			fUtil = fopen(['Uti/Uti', num2str(200+i), '.txt'],'r');
			[Util(i), cnt] = fscanf(fUtil, '%f');
			fclose(fUtil);
		else fprintf('[DEBUG%d] Blade-Utilization fails.\n', i); end
		
		if K==1, [a1,a2]=system(['./blade ', ip, ' t']); % get cpu temperature of a blade
		else [a1,a2]=system(['./blade ', ip(i,:), ' t']); end
		if(a1 == 0)
			fTem = fopen(['Tem/Tem', num2str(200+i), '.txt'],'r');
			[Tem(i), cnt] = fscanf(fTem, '%f');
			fclose(fTem);
		else fprintf('[DEBUG%d] Blade-Temperature fails.\n', i); end
    end
    Util_record(j,1:6) = Util;

	% fpowerflag = fopen('ReadPower/flag.txt','w');
	% fprintf(fpowerflag,'%d\n', j);
    % fclose(fpowerflag);
	pause(1);
    freadpower = fopen('ReadPower/tpower.txt','r'); % tp: actual total power
    [tp, cnt] = fscanf(freadpower, '%f');
    fclose(freadpower);
    
    WR=repmat( 0.5*diag( [Util, 20*ones(1,L)] ),M );
    Ref=Ps-(Ps-tp).*exp(-0.5*[1:P]'); %Reference trajectory
    E=Ref-tp*ones(P,1)+SG*D(1:N); %(Theta*s-E)^2
    b=-tp+SG*D(1:N)+Ps; %Theta*s<=b
    
    % [D,Fval,flag]=fmincon(@(D) (Theta*D-E).'*(Theta*D-E)+(WR*D).'*(WR*D),...
        % Initial,Theta,b,[],[],lb,ub,@(D) mycon(D,Tem,Ts,K),opt);
    [D,Fval,flag]=fmincon(@(D) (Theta*D-E).'*(Theta*D-E)+(WR*D).'*(WR*D),Initial,Theta,b,[],[],lb,ub,[],opt);

    cpu_freq=D(1:K)+freq_max;%s=f-Fmax

    fan_speed=D(K+1:K+L);%compute fan speed

    cpu_freq'
    cpu_freq_record(j,1:6) = cpu_freq';
    fan_speed'
    fan_record(j,1:2) = fan_speed';
    Tem
    Tem_record(j,1:6) = Tem;
    
	C1 = clock;
	rest_time = period - ((C1(4)-C0(4))*3600+(C1(5)-C0(5))*60+(C1(6)-C0(6)));
	fprintf('[Rest Time] = %f\n', rest_time);
	pause(max(0, rest_time));
	C0 = clock;
	
	% ----- Fan Speed Configuration -----\
    fan_power=polyval(fan_power_fit,fan_speed);
    fan_voltage=polyval(fan_voltage_fit,fan_speed-0.01,[],mu);
    for i=1:L
        fwrite(s_port,fan_voltage(i)); %[USB]
    end
	% ----- CPU Frequency Configuration -----\
	for i=1:K,
		% DVFS_LEVEL = num2str( round(cpu_freq(i)*10/4.5)/10 );
		% DVFS_LEVEL(2) = num2str(period);
		DVFS_LEVEL = num2str( round(cpu_freq(i)/4.5) );
		if K==1, [a1,a2]=system(['./blade ', ip, ' ', DVFS_LEVEL]);
		else [a1,a2]=system(['./blade ', ip(i,:), ' ', DVFS_LEVEL]); end
		if(a1 ~= 0) fprintf('[DEBUG] Blade-SetFrequency fails.\n'); end
	end
	% -----------------------------------/
	
    if j<=n,
        fprintf(fp1,'%.2f   ',cpu_freq'); %write the results to the file
        fprintf(fp1,'\n'); %write the results to the file
        fprintf(fp2,'%.2f   ',tp); %write the results to the file
        tp_out=[tp_out,tp];
        Ps_out=[Ps_out,Ps];
        sum_freq=[sum_freq,sum(cpu_freq)];
        fan_out=[fan_out,sum(fan_power)];
    else
        fclose(fp1); %close the file
        fclose(fp2); %close the file
        break;
    end
end

fwrite(s_port,200);%fwrite(s_port,130); %[USB]
fwrite(s_port,200);%fwrite(s_port,70); %[USB]
fclose(s_port); %[USB]

figure;
subplot(1,3,1),plot(tp_out,'kd-','LineWidth',1.5,'MarkerFaceColor','k','MarkerSize',4);
set(gca,'Fontsize',12,'LineWidth',1);hold on;
plot(Ps_out,'r:','LineWidth',1),xlabel('Control Period')
legend('Total Power','Power Constraint','Location','South')
xlim([1,n]),title('Total Power Consumption')
subplot(1,3,2),plot(fan_out,'k','LineWidth',1.5)
set(gca,'Fontsize',12,'LineWidth',1);
xlabel('Control Period')
xlim([1,n]),title('Fan Power')
subplot(1,3,3),plot(sum_freq/K,'k','LineWidth',1.5)
set(gca,'Fontsize',12,'LineWidth',1);
xlim([1,n]),title('Average Frequency')
xlabel('Control Period')
