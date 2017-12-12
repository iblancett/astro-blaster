function main
    % Globals
    triangle = [1, 0; 0, 2; -1, 0];
    rotate_ship(pi/2,triangle);
end

function rotate_ship(theta, shape)
    for i=0:.01:theta
        R = [cos(i) -sin(i); sin(i) cos(i)];
        for row=1:length(shape)
            shape(row,:) = shape(row,:)*R;
        end
        draw_ship(shape)
    end
end

function draw_ship(shape)
    figure(1)
    
    for i = 1:length(shape)-1
        xlim([-5 5])
        ylim([-1 9])        
        line = get_line(shape(i,:), shape(i+1,:));
        plot(line(1,:), line(2,:), 'k')
    end
    xlim([-5 5])
    ylim([-1 9])
    line = get_line(shape(1,:), shape(end,:));
    plot(line(1,:), line(2,:), 'k')
end

function res = get_line(p1, p2)
    theta = atan2( p2(2) - p1(2), p2(1) - p1(1));
    r = sqrt( (p2(1) - p1(1))^2 + (p2(2) - p1(2))^2);
    line = 0:0.01: r;
    x = p1(1) + line*cos(theta);
    y = p1(2) + line*sin(theta);
    res = [x; y];
end
